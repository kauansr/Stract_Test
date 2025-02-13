from flask import Flask, jsonify, render_template, Response
from app.services import Platform_Services
import csv
import io

app = Flask(__name__)

platform_services  = Platform_Services()

@app.route('/')
def home():
    return jsonify({
        "name": "Kauan da Silva",
        "email": "silva4kaka@gmail.com",
        "linkedin": "https://www.linkedin.com/in/kauan-silva1/"
    })

@app.route('/platformas')
def get_platforms():
    return jsonify(platform_services.get_platforms())

@app.route('/<platforma>')
def platform_report(platforma):
    platforma = str(platforma).lower()
    platforms = platform_services.get_platform_data(platforma)
    return render_template("TablePlatform.html", result_table=platforms, platform=platforma)


@app.route('/<platforma>/resumo')
def show_platform_resumo(platforma):
    platforma = str(platforma).lower()
    result_table = platform_services.get_platform_data_resumo(platforma)
    return render_template('TablePlatformResumo.html', result_table=result_table, platform=platforma)



@app.route('/geral')
def geral():
    result_table = platform_services.get_platform_data_geral() 


    if not result_table or len(result_table) < 2:
        return render_template('geral_report.html', columns=[], rows=[])

    columns = result_table[0]  
    rows = result_table[1:]     

    return render_template('geral_report.html', columns=columns, rows=rows)




@app.route('/geral/resumo', methods=["GET"])
def geral_resumo():
    result_table = platform_services.get_platform_data_geral_resumo() 


    if not result_table or len(result_table) < 2:
        return render_template('geral_report.html', columns=[], rows=[])

    columns = result_table[0]  
    rows = result_table[1:]     

    return render_template('geral_report_resumo.html', columns=columns, rows=rows)











# Rotas para exportar csv
@app.route('/export_csv/<platforma>')
def export_csv(platforma):
    
    result_table = platform_services.get_platform_data(platforma)

    if not result_table:
        return "Nenhum dado disponível para exportar", 400

    columns = result_table[0] 
    rows = result_table[1:]     


    output = io.StringIO()
    writer = csv.writer(output)
    
    
    writer.writerow(columns)

    
    writer.writerows(rows)

    
    output.seek(0)  
    return Response(output.getvalue(), mimetype='text/csv', headers={
        'Content-Disposition': f'attachment; filename={platforma}_relatorio.csv'
    })

@app.route('/export_csv_resumo/<platforma>')
def export_csv_resumo(platforma):
    
    result_table = platform_services.get_platform_data_resumo(platforma)

    if not result_table:
        return "Nenhum dado disponível para exportar", 400

    columns = result_table[0]  
    rows = result_table[1:]   

  
    output = io.StringIO()
    writer = csv.writer(output)
    

    writer.writerow(columns)

   
    writer.writerows(rows)

   
    output.seek(0) 
    return Response(output.getvalue(), mimetype='text/csv', headers={
        'Content-Disposition': f'attachment; filename={platforma}_resumo_relatorio.csv'
    })




@app.route('/export_csv_geral')
def export_csv_geral():
    
    result_table = platform_services.get_platform_data_geral()

    if not result_table:
        return "Nenhum dado disponível para exportar", 400

    columns = result_table[0]  
    rows = result_table[1:]    

    
    output = io.StringIO()
    writer = csv.writer(output)

   
    writer.writerow(columns)

    
    writer.writerows(rows)

    
    output.seek(0)

    return Response(output.getvalue(), mimetype='text/csv', headers={
        'Content-Disposition': 'attachment; filename=relatorio_geral.csv'
    })


@app.route('/export_csv_geral_resumo')
def export_csv_geral_resumo():
    
    result_table = platform_services.get_platform_data_geral_resumo()

    if not result_table:
        return "Nenhum dado disponível para exportar", 400

    columns = result_table[0]  
    rows = result_table[1:]    

    
    output = io.StringIO()
    writer = csv.writer(output)

   
    writer.writerow(columns)

    
    writer.writerows(rows)

    
    output.seek(0)

    return Response(output.getvalue(), mimetype='text/csv', headers={
        'Content-Disposition': 'attachment; filename=relatorio_geral_resumo.csv'
    })



if __name__ == '__main__':
    app.run(debug=True)