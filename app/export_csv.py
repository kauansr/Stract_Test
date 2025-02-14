import csv
import io

def download_csv(result_table):
    """
    Faz a tabela virar o arquivo .csv

    args:
    - result_table: É a tabela que sera transformada em csv.

    return:
    - output.get_value(): O arquivo csv.
    """

    if not result_table:
        return "Nenhum dado disponível para exportar", 400

    columns = result_table[0]  
    rows = result_table[1:]   

  
    output = io.StringIO()
    writer = csv.writer(output)
    

    writer.writerow(columns)

   
    writer.writerows(rows)

   
    output.seek(0)

    return output.getvalue() 