from app.api import get_requests

class ApiClient:
    def get_platforms(self):
        response = get_requests('/platforms')
        return response
    
    def get_accounts(self, platform):
        response = get_requests(f'/accounts?platform={platform}')
        return response
    
    def get_fields(self, platform):
        all_fields = []
        current_page = 1

        while True:
        
            if platform == 'meta_ads':
                response = get_requests(f'/fields?platform={platform}&page={current_page}')
            else:
                response = get_requests(f'/fields?platform={platform}')

            fields = response.get('fields', [])
            pagination = response.get('pagination', {})

            
            
            all_fields.extend(fields)

            current_page = pagination.get('current', 1)
            total_pages = pagination.get('total', 1)

            if current_page >= total_pages:
                break

            current_page += 1

        return all_fields

    
    def get_insights(self, platform, account, token, fields):
        response = get_requests(f'/insights?platform={platform}&account={account}&token={token}&fields={fields}')
        return response