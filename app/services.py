from app.api_client import ApiClient
import concurrent.futures


class Platform_Services:
    def __init__(self):
        self.apiclient = ApiClient()
    

    

    def get_platforms(self):
        """
        Pega os dados das plataformas

        return:
        - Json: -> retorna os dados da api em json.        
        """
        return self.apiclient.get_platforms()


    def get_platform_data(self, platform):
        """
        Funcao para pegar dados por plataforma

        args:
        - platform: str -> o nome da plataforma

        Return:
        - result_table: list -> lista de plataforma, ad name, nome e os outros dados de insight
        """
        platforms = {
                "facebook": 'meta_ads',
                'google': 'ga4',
                'tiktok': 'tiktok_insights'
                }

        accounts = self.apiclient.get_accounts(platforms[platform]) 
        fields = self.apiclient.get_fields(platforms[platform]) 

        result_table = []

        columns_fields = []
        

        columns = ['Platform', 'Ad Name', 'Account Name']

        for field in fields:
            columns_fields.append(field['value'])

            if field['text'] != 'Ad Name':
                columns.append(field['text'])  
        
        result_table.append(columns)

        fields_values = ','.join([i for i in columns_fields if i != ''])


        for account in accounts['accounts']:
            account_name = account['name']

            insights = self.apiclient.get_insights(platforms[platform], account['id'], account['token'], fields_values)

            for insight in insights['insights']:
                ad_name = str(insight.get('adName', insight.get('ad_name', 'N/A')))
            
                row = [platform, ad_name, account_name]

                for field in fields:
                    if field['value'] not in ['adName', 'ad_name']:
                        field_value = insight.get(field['value'], 'N/A') 
                        row.append(field_value)

                result_table.append(row)

        return result_table



    def get_platform_data_resumo(self, platform):
        """
        Função para pegar dados agregados por plataforma, com uma linha por conta.
        As colunas numéricas serão somadas e as colunas de texto ficam vazias.
        
        Args:
        - platform: str -> o nome da plataforma
        
        Return:
        - result_table: list -> lista de plataforma, ad name, nome e os outros dados de insight
        """
        platforms = {
            "facebook": 'meta_ads',
            'google': 'ga4',
            'tiktok': 'tiktok_insights'
        }

       
        accounts = self.apiclient.get_accounts(platforms[platform]) 
        fields = self.apiclient.get_fields(platforms[platform]) 

        result_table = []

        
        columns = ['Platform', 'Ad Name', 'Account Name']  
        columns.extend([field['text'] for field in fields if field['text'] != 'Ad Name']) # pra n ter duplicata de adname coluna
        result_table.append(columns)

        
        accounts_data = {}

        fields_values = ','.join([field['value'] for field in fields if field['value'] != 'adName' and field['value'] != 'ad_name'])

        for account in accounts['accounts']:
            account_name = account['name']

            
            insights = self.apiclient.get_insights(platforms[platform], account['id'], account['token'], fields_values)

            for insight in insights['insights']:

                if account_name not in accounts_data:
                    accounts_data[account_name] = {
                        'Platform': platform,
                        'Ad Name': '',
                        'Account Name': account_name,
                        'data': {field['value']: 0 if isinstance(insight.get(field['value']), (int, float)) else '' for field in fields}
                    }

                
                for field in fields:
                    field_value = insight.get(field['value'], None)

                    if isinstance(field_value, (int, float)):  
                        accounts_data[account_name]['data'][field['value']] += field_value

                    elif field_value is not None:  
                        if accounts_data[account_name]['data'][field['value']] == '':
                            accounts_data[account_name]['data'][field['value']] = '' 

        
        for account_name, data in accounts_data.items():
            row = [data['Platform'], data['Ad Name'], data['Account Name']]

            for field in fields:
                if field['value'] != 'adName' and field['value'] != 'ad_name':
                    
                    if isinstance(data['data'].get(field['value'], ''), str):
                        row.append('')
                    else:
                        row.append(data['data'].get(field['value'], 0)) 
            result_table.append(row)

        return result_table


    


    def get_platform_data_geral(self):
        """
        Pega dados de todas as plataformas (Facebook, Google, TikTok) e gera o relatório unificado.

        Return:
        - result_table: list -> Uma lista com todos os dados das plataformas e usuários.
        """
        platforms = {
            "facebook": 'meta_ads',
            'google': 'ga4',
            'tiktok': 'tiktok_insights'
        }

        result_table = []
        columns_fields = ['Plataforma', 'Ad Name', 'Account Name']
        all_fields = set()

        for plat_name, plat_key in platforms.items():
            accounts = self.apiclient.get_accounts(plat_key)  
            fields = self.apiclient.get_fields(plat_key)  

            for field in fields:
                if field['text'] != 'Ad Name':
                    all_fields.add(field['text'])

        all_fields = sorted(list(all_fields))


        result_table.append(columns_fields + all_fields)

        # Identificar o índice da coluna "Cost Per Click" no header da tabela
        cost_column_index = columns_fields + all_fields
        cost_column_index = cost_column_index.index("Cost Per Click")  # Encontrando a posição da coluna

        for plat_name, plat_key in platforms.items():
            accounts = self.apiclient.get_accounts(plat_key)  
            fields = self.apiclient.get_fields(plat_key)  

            field_mapping = {field['text']: field['value'] for field in fields}

            for account in accounts['accounts']:
                account_name = account['name']

                fields_values = ','.join([field['value'] for field in fields])

                insights = self.apiclient.get_insights(plat_key, account['id'], account['token'], fields_values)

                for insight in insights['insights']:
                    ad_name = str(insight.get('adName', insight.get('ad_name', 'N/A')))
                    
                    row = [plat_name, ad_name, account_name]

                
                    for field_name in all_fields:
                        field_value = ''

                        if field_name in field_mapping:
                            field_value = insight.get(field_mapping[field_name], 'N/A')

                        row.append(field_value)

                   
                    if plat_name == 'google':
                        spend = insight.get('cost', 0)
                        clicks = insight.get('clicks', 0)
                        cpc = round(spend / clicks, 3)
                        row[cost_column_index] = cpc  

                    result_table.append(row)

        return result_table





    def get_platform_data_geral_resumo(self):
        """
        Pega dados de todas as plataformas (Facebook, Google, TikTok) e gera o relatório unificado.

        Return:
        - result_table: list -> Uma lista com todos os dados das plataformas e usuários.
        """
        platforms = {
            "facebook": 'meta_ads',
            'google': 'ga4',
            'tiktok': 'tiktok_insights'
        }

        result_table = []
        columns_fields = ['Plataforma', 'Ad Name', 'Account Name']
        all_fields = set()

       
        for plat_name, plat_key in platforms.items():
            accounts = self.apiclient.get_accounts(plat_key)  
            fields = self.apiclient.get_fields(plat_key)  

            for field in fields:
                if field['text'] != 'Ad Name':
                    all_fields.add(field['text'])

        all_fields = sorted(list(all_fields))
        result_table.append(columns_fields + all_fields)

      
        cost_column_index = columns_fields + all_fields
        cost_column_index = cost_column_index.index("Cost Per Click")

        aggregated_data = {}

       
        for plat_name, plat_key in platforms.items():
            accounts = self.apiclient.get_accounts(plat_key)  
            fields = self.apiclient.get_fields(plat_key)  

            field_mapping = {field['text']: field['value'] for field in fields}

           
            for account in accounts['accounts']:
                

              
                fields_values = ','.join([field['value'] for field in fields])

            
                insights = self.apiclient.get_insights(plat_key, account['id'], account['token'], fields_values)

                for insight in insights['insights']:
                    

                  
                    if plat_name not in aggregated_data:
                        aggregated_data[plat_name] = {'Plataforma': plat_name, 'Ad Name': '', 'Account Name': '', 'cost': 0, 'clicks': 0}

                    row = aggregated_data[plat_name]

                 
                    for field_name in all_fields:
                        field_value = insight.get(field_mapping.get(field_name, ''), '')

                        
                        if isinstance(field_value, (int, float)):  
                            row[field_name] = row.get(field_name, 0) + field_value

                   
                    if not row['Ad Name']:
                        row['Ad Name'] = ''

                    if not row['Account Name']:
                        row['Account Name'] = ''


                    row['cost'] += insight.get('cost', 0)
                    row['clicks'] += insight.get('clicks', 0)



        for plat_name, row in aggregated_data.items():
            if plat_name == 'google':

                total_cpc = 0

                spend = insight.get('cost', 0)
                clicks = insight.get('clicks', 0)
                pre_cpc = round(spend / clicks, 3)

                total_cpc += pre_cpc

                cpc = total_cpc
                row["Cost Per Click"] = cpc

            
            result_row = [row['Plataforma'], row['Ad Name'], row['Account Name']]
            for field in all_fields:
                result_row.append(row.get(field, ''))  
        
           
            result_table.append(result_row)

        return result_table