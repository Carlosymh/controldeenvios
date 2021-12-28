from flask import Flask, render_template, request, redirect, url_for, flash, session, make_response, Response, jsonify
import io
import csv
from fpdf import FPDF
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date
import hashlib
import qrcode 
import csv

app = Flask(__name__)

#MySQL Connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'insumos'
mysql = MySQL(app)

# settings
app.secret_key = 'mysecretkey'


#Direccion Principal 
@app.route('/')
def Index():
  try:
    if 'FullName' in session:
      return redirect('/home')
    else:
      return render_template('index.html')
  except:
      return render_template('index.html')

#Valida de usuario
@app.route('/validar_usuario', methods=['POST'])
def validarusuaro():
    if request.method == 'POST':
      usuario =  request.form['user']
      cur = mysql.connection.cursor()
      cur.execute('SELECT * FROM usuarios WHERE Usuario = \'{}\' LIMIT 1 '.format(usuario))
      data = cur.fetchall()
      if len(data) > 0 :
        username = data[0][1]
        user = data[0][3]
        return render_template('inicio.html',username=username,user=user)
      else:
        return render_template('index.html')    

#Validacion de Contraseña
@app.route('/validar_contrasena/<user>', methods=['POST'])
def validarcontrasena(user):
    if request.method == 'POST':
      usuario =  user
      password = request.form['password']
      cur = mysql.connection.cursor()
      cur.execute('SELECT * FROM usuarios WHERE Usuario = \'{}\' LIMIT 1 '.format(usuario))
      data = cur.fetchall()
      if len(data) > 0 :
          if check_password_hash(data[0][6],password):
            session['UserName'] = data[0][1]
            session['FullName'] = data[0][1] + data[0][2]
            session['User'] = data[0][3]
            session['FcName'] = data[0][4]
            session['SiteName'] = data[0][5]
            session['Rango'] = data[0][7]
            return redirect('/home')
          else:
            flash('Contraseña Incorrecta')
            return render_template('index.html')
      else:
        return render_template('index.html')   

#Pagina Principal
@app.route('/home',methods=['POST','GET'])
def home():
  if 'FullName' in session:
    return render_template('home.html',Datos = session)
  else:
    flash("Inicia Sesion")
    return render_template('index.html')

#Formulario de Registro
@app.route('/f_r_f',methods=['POST','GET'])
def Recibo_full_form():
  if 'FullName' in session:
    return render_template('form/f_r_f.html',Datos = session)
  else:
    return render_template('index.html')

#formulario de Prealert
@app.route('/f_p',methods=['POST','GET'])
def Prealert_form():
  if 'FullName' in session:
    return render_template('form/f_p.html',Datos = session)
  else:
    return render_template('index.html')

#formulario de ordenes Prealert
@app.route('/f_r_p_s',methods=['POST','GET'])
def Registr_Prealert_service_form():
  if 'FullName' in session:
    now1 = datetime.now()
    prealert_key = "CE"+str(now1)+"P"
    key = prealert_key.replace(" ","")
    key_ = key.replace(":","")
    key_p = key_.replace(".","")
    key_pa = key_p.replace("-","")
    session['key_pa']= key_pa
    return render_template('form/f_r_p_s.html',Datos = session)
  else:
    return render_template('index.html')

#formulario Planning Fullfilment
@app.route('/f_p_f',methods=['POST','GET'])
def Planning_full_form():
  if 'FullName' in session:
    return render_template('form/f_p_f.html',Datos = session)
  else:
    flash("Inicia Sesion")
    return render_template('index.html')

#formulario ordenes no Procesables 
@app.route('/f_n_p',methods=['POST','GET'])
def No_procesable_form():
  if 'FullName' in session:
    return render_template('form/f_n_p.html',Datos = session)
  else:
    flash("Inicia Sesion")
    return render_template('index.html')

#formulario entradas Service Center
@app.route('/f_e_s',methods=['POST','GET'])
def Entradas_Service_form():
  if 'FullName' in session:
    return render_template('form/f_e_s.html',Datos = session)
  else:
    flash("Inicia Sesion")
    return render_template('index.html')

#fomulari salidas Service Center
@app.route('/f_s_s',methods=['POST','GET'])
def Salidas_Service_form():
  if 'FullName' in session:
    return render_template('form/f_s_s.html',Datos = session)
  else:
    flash("Inicia Sesion")
    return render_template('index.html')

#formulario Planning
@app.route('/f_planning',methods=['POST','GET'])
def Planning_form():
  if 'FullName' in session:
    return render_template('form/f_planning.html',Datos = session)
  else:
    flash("Inicia Sesion")
    return render_template('index.html')

#formulario Planning Cross Dock 
@app.route('/f_p_xd',methods=['POST','GET'])
def Planning_Cross_form():
  if 'FullName' in session:
    return render_template('form/f_p_xd.html',Datos = session)
  else:
    flash("Inicia Sesion")
    return render_template('index.html')

#formulario Actualizacion de estatus ordenes no Procesables 
@app.route('/f_a_o',methods=['POST','GET'])
def Actualizacion_ordenes_noprocesables():
  if 'FullName' in session:
    return render_template('form/f_a_o.html',Datos = session)
  else:
    flash("Inicia Sesion")
    return render_template('index.html')

#Redirigie a el Formulario de Registro de Usuarios 
@app.route('/registro',methods=['POST','GET'])
def registro():
  try:
    if session['Rango'] == 'Administrador':
      return render_template('registro.html', Datos = session)
    else:
      flash("Acseso Denegado")
    return render_template('index.html')
  except:
    flash("Inicia Secion")
    return render_template('index.html')

#Registro de Usuarios 
@app.route('/registrar',methods=['POST'])
def registrar():
  try:
      if request.method == 'POST':
        nombre =  request.form['nombre']
        apellido =  request.form['apellido']
        rango = request.form['rango']
        ltrabajo =  request.form['ltrabajo']
        cdt = request.form['cdt']
        usuario =  request.form['usuario']

        password = _create_password(request.form['pass'])
        password2 = _create_password(request.form['pass2'])
        
        if check_password_hash(password,request.form['pass']) and check_password_hash(password,request.form['pass2']):
          
          cur = mysql.connection.cursor()
          cur.execute('SELECT * FROM usuarios WHERE Usuario = \'{}\'  LIMIT 1 '.format(usuario,password))
          data = cur.fetchall()
          if len(data) > 0:
            flash("El Usuario Ya Existe")
            return render_template('registro.html',Datos =session)
          else:
            cur = mysql.connection.cursor()
            cur.execute('INSERT INTO `usuarios` (Nombre,Apellido, Usuario, ltrabajo, cdt, contraseña, Rango) VALUES (%s,%s,%s,%s,%s,%s,%s)',(nombre,apellido,usuario,ltrabajo,cdt,password,rango))
            mysql.connection.commit()
            flash("Registro Correcto")
            return render_template('registro.html',Datos =session)
        else:
          flash("Las Contraceñas no Cionciden")
          return render_template('registro.html',Datos =session)
  except:
    return render_template('registro.html',Datos =session)
def _create_password(password):
   return generate_password_hash(password,'pbkdf2:sha256:30',30)

#Registros entradas Service Center
@app.route('/registro_svcs_entrada',methods=['POST'])
def registro_s_e():
  try:
      if request.method == 'POST':
        cdt =  session['SiteName']
        Pallets_en_buen_estado =  request.form['Pallets_en_buen_estado']
        Pallets_en_mal_estado = request.form['Pallets_en_mal_estado']
        Pallets_Totales_Recibidos = int(Pallets_en_buen_estado)+int(Pallets_en_mal_estado)
        Gaylords_en_buen_estado = request.form['Gaylords_en_buen_estado']
        Gaylords_en_mal_estado =  request.form['Gaylords_en_mal_estado']
        Gaylords_Totales_Recibidos = int(Gaylords_en_buen_estado)+int(Gaylords_en_mal_estado)
        cajas = request.form['cajas']
        costales =  request.form['costales']
        Centro_de_Origen = request.form['Centro_de_Origen']
        usuario =  session['FullName']
        now = datetime.now()
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO entrada_svcs (Centro_de_trabajo_donde_te_encuentras, Pallets_Totales_Recibidos, Pallets_en_buen_estado, Pallets_en_mal_estado, Gaylords_Totales_Recibidos, Gaylords_en_buen_estado, Gaylords_en_mal_estado, Cajas, Costales, Centro_de_Origen, Responsable, Fecha_Creación, Fecha_Hora) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(cdt,Pallets_Totales_Recibidos,Pallets_en_buen_estado,Pallets_en_mal_estado,Gaylords_Totales_Recibidos,Gaylords_en_buen_estado,Gaylords_en_mal_estado,cajas,costales,Centro_de_Origen,usuario,now,now))
        mysql.connection.commit() 
        flash("Registro Exitoso")
        return render_template('form/f_e_s.html',Datos = session)
      else:
        flash("No has enviado un registro")
        return render_template('form/f_e_s.html',Datos = session)
  except:
    flash("Llena todos los Campos Correctamente")
    return render_template('form/f_e_s.html',Datos = session)

# Registro de Salidas Service Center
@app.route('/registro_svcs_salida',methods=['POST'])
def registro_s_s():
  try:
      if request.method == 'POST':
        cdt =  session['SiteName']
        Tarimas_enviadas = request.form['Tarimas_enviadas']
        Gaylord_Enviados =  request.form['Gaylord_Enviados']
        cajas = request.form['cajas']
        costales =  request.form['costales']
        Cross_Dock = request.form['Cross_Dock']
        usuario =  session['FullName']
        now = datetime.now()
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO salida_svcs (Centro_de_trabajo_donde_te_encuentras, Tarimas_enviadas, Gaylord_Enviados, cajas, costales, Cross_Dock, Responsable, Fecha_Creación	, Fecha_Hora) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)',(cdt,Tarimas_enviadas,Gaylord_Enviados,cajas,costales,Cross_Dock,usuario,now,now))
        mysql.connection.commit() 
        flash("Registro Exitoso")
        return render_template('form/f_s_s.html',Datos = session)
      else:
        flash("No has enviado un registro")
        return render_template('form/f_s_s.html',Datos = session)
  except:
    flash("Llena todos los Campos Correctamente")
    return render_template('form/f_s_s.html',Datos = session)

# Registro Prealert ordenes 
@app.route('/registro_prealert_ordenes',methods=['POST'])
def registroPrealertOrdenes():
  try:
      if request.method == 'POST':
        key_pa = session['key_pa']
        OrigenFc = session['FcName']
        OrigenSite = session['SiteName']
        Orden = request.form['Orden']
        Paquetera = request.form['Paquetera']
        reponsable = session['FullName']
        now = datetime.now()
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO prealert (ID_Envio_Prealert, Origen, SiteName, Orden, Paquetera, Responsable, Fecha, fecha_hora) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)',(key_pa, OrigenFc, OrigenSite, Orden, Paquetera, reponsable, now, now))
        mysql.connection.commit() 
        flash("Registro Exitoso")
        return render_template('form/f_r_p_s.html',Datos = session)
      else:
        flash("No has enviado un registro")
        return render_template('form/f_r_p_s.html',Datos = session)
  except:
    flash("Llena todos los Campos Correctamente")
    return render_template('form/home.html',Datos = session)

#registro Envio Prealert Prealert
@app.route('/registro_prealert',methods=['POST'])
def registroPrealert():
  try:
      if request.method == 'POST':
        session['key_pa']= request.form['key_pa']
        Facility=request.form['Facility']
        if Facility[0:2]=="MX":
          session['destinoPrealert'] = "Cross Dock"
        else:
          session['destinoPrealert'] = "Fullfilment"
        session['SiteDestinoPrealert'] = request.form['Facility']
        session['TransportePrealert'] = request.form['Transporte']
        session['TrasportistaPrealert'] =  request.form['Trasportista']
        session['PlacasPrealert'] = request.form['Placas']
        Marchamo = request.form['Marchamo']
        reponsable = session['FullName']
        now = datetime.now()
        cur = mysql.connection.cursor()
        cur.execute("""UPDATE prealert SET  Destino= %s, SiteName_Destino= %s, EmpresaTransporte= %s, Transportista= %s, Placas= %s, Marchamo= %s, Responsable= %s,  Fecha= %s, fecha_hora= %s WHERE ID_Envio_Prealert = %s  AND SiteName = %s""",(session['destinoPrealert'],session['SiteDestinoPrealert'],session['TransportePrealert'],session['TrasportistaPrealert'],session['PlacasPrealert'],Marchamo,reponsable,now,now,session['key_pa'],session['SiteName']))
        mysql.connection.commit()
        flash("Registro Exitoso")
        return render_template('actualizacion/finalizado.html',Datos = session)
      else:
        flash("No has enviado un registro")
        return render_template('form/f_p.html',Datos = session)
  except:
    flash("Llena todos los Campos Correctamente")
    return render_template('form/f_p.html',Datos = session)

#confirmacionde Finalizacion Prealert
@app.route("/FinalizarPrealert",methods=['POST','GET'])
def finalizarPallet():
  try:
    if 'FullName' in session:
      return render_template("form/finalizar.html", Datos =session)
  except:  
    return render_template("home.html",Datos=session)

#confirmacionde Finalizacion Prealert Ordenes 
@app.route("/FinalizarPrealertOrdenes",methods=['POST','GET'])
def finalizarPalletOrdenes():
  try:
    return render_template('actualizacion/finalizado.html',Datos = session)
  except:
    flash("No has enviado un registro")
    return render_template('form/finalizar.html',Datos = session)


@app.route('/registro_fcs_recibo',methods=['POST'])
def registro_fcs_r():
  try:
      if request.method == 'POST':
        cdt =  session['SiteName']
        paquetera = request.form['paquetera']
        no_gia =  request.form['no_gia']
        no_paquete = request.form['no_paquete']
        tipo_paquete =  request.form['tipo_paquete']
        estatus =  request.form['estatus']
        razon_rechazo = request.form['razon_rechazo']
        usuario =  session['FullName']
        now = datetime.now()
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO recibo_fc (Fulfillment, responsable, paquetera, no_gia, no_paquete, tipo_paquete, estatus, razon_rechazo, fecha_hora, dia) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(cdt,usuario,paquetera,no_gia,no_paquete,tipo_paquete,estatus,razon_rechazo,now,now))
        mysql.connection.commit() 
        flash("Registro Exitoso")
        return render_template('form/f_r_f.html',Datos = session)
      else:
        flash("No has enviado un registro")
        return render_template('form/f_r_f.html',Datos = session)
  except:
    flash("Llena todos los Campos Correctamente")
    return render_template('form/f_r_f.html',Datos = session)


@app.route('/registro_ordenes',methods=['POST'])
def registro_o():
  try:
      if request.method == 'POST':

        usuario =  session['UserName']
        Paquetera = request.form['Paquetera']
        orden =  request.form['orden']
        Pallet = request.form['Pallet']
        Tipo =  request.form['Tipo']
        cdt =  session['SiteName']
        Estatus =  request.form['Estatus']
        Service_Center = request.form['Service_Center']

        if Service_Center =='SAG1':
          region = 'Bajio'
        elif Service_Center =='STJ1': 
          region = 'Norte Pacifico '
        elif Service_Center =='SLP1':
          region = 'Norte Pacifico '
        elif Service_Center=='STG1':
          region = 'Sureste'
        elif Service_Center=='SCJ1':
          region = 'Noroeste'
        elif Service_Center=='SCH1':
          region = 'Noroeste'
        elif Service_Center=='SMX2':
          region = 'Metro norte'
        elif Service_Center=='SMX1':
          region = 'Metro norte'
        elif Service_Center=='SMX3':
          region = 'Metro sur'
        elif Service_Center=='SMX5':
          region = 'Metro norte'
        elif Service_Center=='SMX4':
          region = 'Metro sur'
        elif Service_Center=='SMX6':
          region = 'Metro norte'
        elif Service_Center=='STR1':
          region = 'Noroeste'
        elif Service_Center=='SCQ1':
          region = 'Centro'
        elif Service_Center=='SZL1': 
          region = 'Centro'
        elif Service_Center=='SDG1':
          region = 'Noroeste'
        elif Service_Center=='SHP1':
          region = 'Metro norte'
        elif Service_Center=='SLE1':
          region = 'Bajio'
        elif Service_Center=='SGR1':
          region = 'Metro sur'
        elif Service_Center=='SGD1':
          region = 'Centro'
        elif Service_Center=='STL1':
          region= 'Metro norte'
        elif Service_Center=='SML1':
          region= 'Bajio'
        elif Service_Center=='SCV1':
          region= 'Metro sur'
        elif Service_Center=='SPV1':
          region= 'Centro'
        elif Service_Center=='STN1':
          region= 'Centro'
        elif Service_Center=='SOX1':
          region= 'Golfo'
        elif Service_Center=='SPB1':
          region= 'Golfo'
        elif Service_Center=='SQR1':
          region= 'Bajio'
        elif Service_Center=='SCN1':
          region= 'Sureste'
        elif Service_Center=='SSL1':
          region= 'Bajio'
        elif Service_Center=='SCU1':
          region= 'Norte Pacifico '
        elif Service_Center=='SMZ1':
          region= 'Centro'
        elif Service_Center=='SMO1': 
          region= 'Norte Pacifico'
        elif Service_Center=='SHM1': 
          region= 'Norte Pacifico '
        elif Service_Center=='SVH1':
          region= 'Sureste'
        elif Service_Center=='SVR1':
          region= 'Golfo'
        elif Service_Center=='SPZ1':
          region= 'Golfo'
        elif Service_Center=='SMD1':
          region= 'Sureste'
        elif Service_Center=='SZC1':
          region= 'Noroeste'
        elif Service_Center=='SLP1_A':
          region= 'Norte Pacifico '
        elif Service_Center=='SMZ1_A':
          region= 'Centro'
        elif Service_Center=='SCN1_A':
          region= 'Sureste'
        elif Service_Center=='SMX3_S':
          region= 'Metro sur'
        elif Service_Center=='STJ1_A':
          region= 'Norte Pacifico '
        elif Service_Center=='SCU1_A':
          region= 'Norte Pacifico '
        elif Service_Center=='SMO1_A':
          region= 'Norte Pacifico '
        elif Service_Center=='SHM1_A':
          region= 'Norte Pacifico '
        elif Service_Center=='SCJ1_A':
          region= 'Noroeste'
        elif Service_Center=='SMD1_A':
          region= 'Sureste'
        elif Service_Center=='SMX1_S':
          region= 'Metro norte'
        elif Service_Center=='SCH1_A':
          region= 'Noroeste'
        elif Service_Center=='SMX4_S': 
          region= 'Metro sur'
        elif Service_Center=='SMX5_S':
          region= 'Metro norte'
        elif Service_Center=='SMX2_S':
          region= 'Metro norte' 
        elif Service_Center=='SMX6_S':
          region= 'Metro norte'
        elif Service_Center=='slw1':
          region= 'Noreste'
        elif Service_Center=='smt1':
          region= 'Noreste'
        elif Service_Center=='srx1':
          region= 'Noreste'
        elif Service_Center=='sma1':
          region= 'Noreste'
        elif Service_Center=='sta1':
          region= 'Noreste'
        elif Service_Center=='snl1':
          region= 'Noreste'
        elif Service_Center=='99MLM':
          region= '99minutos'
        elif Service_Center=='DHLSU2':
          region= 'DHL'
        elif Service_Center=='DHLJC1':
          region= 'DHL'
        elif Service_Center=='ESTMLM':
          region= 'Estafeta'
        elif Service_Center=='FDXXS2':
          region= 'FedEx'
        elif Service_Center=='FDXSO1':
          region= 'FedEx'
        elif Service_Center=='PQXMLM':
          region= 'Paquetexpress'
        elif Service_Center=='SG2':
          region= 'Centro'
        elif Service_Center=='SJA1':
          region= 'Golfo'
        elif Service_Center=='SCT1':
          region= 'Sureste'
        elif Service_Center=='SMI1':
          region= 'Sureste'
        elif Service_Center=='SBJ1':
          region= 'Bajio'
        elif Service_Center=='SVM1':
          region= 'Noreste'
        elif Service_Center=='SMT2':
          region= 'Noreste'
        elif Service_Center=='SMX7':
          region= 'Metro sur'
        elif Service_Center=='SMX7_S':
          region= 'Metro sur'
        elif Service_Center=='SDC1':
          region= 'Golfo'
        elif Service_Center=='SCP1':
          region= 'Sureste'
        elif Service_Center=='SCP1_A':
          region= 'Sureste'
        elif Service_Center=='STP1':
          region= 'Sureste'
        elif Service_Center=='STR1_A':
          region= 'Noroeste'
        elif Service_Center=='SPD1':
          region= 'Noroeste'
        elif Service_Center=='SXL1':
          region= 'Norte Pacifico'
        elif Service_Center=='SCE1':
          region= 'Norte Pacifico '
        elif Service_Center=='SJD1':
          region= 'Norte Pacifico'
        elif Service_Center=='SCY1':
          region= 'Bajio'
        elif Service_Center=='SLZ1':
          region= 'Bajio'
        elif Service_Center=='SGD1_S':
          region= 'Centro'
        elif Service_Center=='SGD2_S':
          region= 'Centro'
        elif Service_Center=='SMT1_S':
          region= 'Noreste'
        elif Service_Center=='SMT2_S':
          region= 'Noreste'
        elif Service_Center=='FedEx':
          region= 'FedEx'
        elif Service_Center=='DHL':
          region= 'DHL'
        elif Service_Center=='Estafeta':
          region= 'Estafeta'
        elif Service_Center=='Paquete Express':
          region= 'Paquete Express'
        elif Service_Center=='sgd2':
          region= 'Centro'
        elif Service_Center=='99 Minutos':
          region= '99 Minutos'

        ticket = request.form['ticket']
        fechatiket =  request.form['fechatiket']
        Comentario =  request.form['Comentario']
        estatus_orden = 'Pendiente'
        now = datetime.now()
        semana = now.isocalendar()
        meses= ('Null','Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiempbre','Octubre','Noviebre','Diciembre')
        mes = meses[now.month]
        Responsable =  session['FullName']
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM ordenes_no_procesables WHERE orden = \'{}\' AND estatus_orden = \'{}\' LIMIT 1 '.format(orden,estatus_orden))
        data = cur.fetchall()
        if len(data)>0:
          flash("Ya Existe un Ticket Pendiente para esta Orden")
          return render_template('form.html',Datos = session)
        elif len(orden)>0 and len(ticket)>0 and len(fechatiket)>0:
          cur = mysql.connection.cursor()
          cur.execute('INSERT INTO ordenes_no_procesables (usuario_wms, paquetera, orden, pallet, tipo, fulfillment_origen, estatus, service_center, region, ticket, fecha_ticket, estatus_orden, Comentario, semana, mes, responsable, fecha_hora, fecha) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(usuario,Paquetera,orden,Pallet,Tipo,cdt,Estatus,Service_Center,region,ticket,fechatiket,estatus_orden,Comentario,semana[1],mes,Responsable,now,now))
          mysql.connection.commit() 
          flash("Registro Exitoso")
          return render_template('form/f_n_p.html',Datos = session)
        else:
          flash("Llena Todos Los Datos")
          return render_template('form/f_n_p.html',Datos = session)
      else:
        flash("No has enviado un registro")
        return render_template('form/f_n_p.html',Datos = session)
  except:
        flash("No has enviado un registro")
        return render_template('form/f_n_p.html',Datos = session)


@app.route('/registro_planing',methods=['POST'])
def registro_p():
  try:
      if request.method == 'POST':
        Fecha_agendada = request.form['Fecha_agendada']
        codigo_sku = int(request.form['codigo_sku'])
        if codigo_sku == 10053:
          descripcion = 'Caja Gaylord'
        elif codigo_sku == 10060:
          descripcion = 'Tarima Madera'
        piezas_p = request.form['piezas_p']
        unidades = request.form['unidades']
        datos_de_la_unidad = request.form['datos_de_la_unidad']
        operador = request.form['operador']
        Origen = session['FcName']
        destino = request.form['destino']
        estatus = 'Pendiente'
        usuario = session['FullName']
        now = datetime.now()
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO planing (Fecha_agendada, codigo_sku, descripción, piezas_p, unidades, datos_de_la_unidad, operador, origen, destino,	reponsable, status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(Fecha_agendada,codigo_sku,descripcion,piezas_p,unidades,datos_de_la_unidad,operador,Origen,destino,usuario,estatus))
        mysql.connection.commit() 
        flash("Registro Exitoso")
        return render_template('form/f_planning.html',Datos = session)
      else:
        flash("No has enviado un registro")
        return render_template('form/f_planning.html',Datos = session)
  except:
    flash("Llena todos los Campos Correctamente")
    return render_template('form/f_planning.html',Datos = session)


@app.route('/a_p_f',methods=['POST'])
def actualizacion_planning_full():
  try:
      if request.method == 'POST':
          id_planing = request.form['id_planing']
          cur = mysql.connection.cursor()
          cur.execute('SELECT * FROM planing WHERE id_planing = \'{}\' LIMIT 1 '.format(id_planing))
          data = cur.fetchall()
          if len(data)>0:
            return render_template('actualizacion/a_p_f.html',Datos = session,Info = data)
          else:
            flash("ID Invalido")
            return render_template('home.html',Datos = session)
      else:
        flash("No has enviado un registro")
        return render_template('home.html',Datos = session)
  except:
    flash("Llena todos los Campos Correctamente")
    return render_template('home.html',Datos = session)


@app.route('/a_p_xd',methods=['POST'])
def actualizacion_planning_cross():
  try:
      if request.method == 'POST':
        id_planing = request.form['id_planing']
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM planing WHERE id_planing = \'{}\' LIMIT 1 '.format(id_planing))
        data = cur.fetchall()
        if len(data)>0:
          id=data[0][0]
          status ='Procesando'
          now = datetime.now()
          responsable=session['FullName']
          cur = mysql.connection.cursor()
          cur.execute("""
          UPDATE planing
          SET hora_inicio_de_carga = %s,
          status = %s,
          responsable_xd = %s
          WHERE id_planing  = %s
          """,(now,status,responsable,id))
          mysql.connection.commit()
          return render_template('actualizacion/a_p_xd.html',Datos = session,Info = data)
        else:
          flash("ID Invalido")
          return render_template('home.html',Datos = session)
      else:
        flash("No has enviado un registro")
        return render_template('home.html',Datos = session)
  except:
    flash("Llena todos los Campos Correctamente")
    return render_template('home.html',Datos = session)


@app.route('/a_o_np',methods=['POST'])
def actualizacion_ordenes_no_procesables():
  try:
      if request.method == 'POST':
        orden = request.form['orden']
        status = 'Pendiente'
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM ordenes_no_procesables WHERE orden = {}  LIMIT 1 '.format(orden))
        data = cur.fetchall()
        if len(data)>0:
          return render_template('actualizacion/a_o_np.html',Datos = session,Info = data)
        else:
          flash("Numero de Orden Invalido")
          return render_template('home.html',Datos = session)
      else:
        flash("No has enviado un registro")
        return render_template('home.html',Datos = session)
  except:
    flash("Llena todos los Campos Correctamente")
    return render_template('home.html',Datos = session)


@app.route('/r_a_p_f',methods=['POST'])
def registro_actalizacion_planning_full():
  try:
    if request.method == 'POST':
        id =  request.form['id']
        estatus = 'Enviado'
        usuario = session['FullName']
        now = datetime.now()
        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE planing
        SET status = %s,
        arribo_a_fc_destino = %s,
        responsable_fc = %s
        WHERE id_planing = %s
        """,(estatus,now,usuario,id))
        mysql.connection.commit()
        flash("Registro Exitoso")
        return render_template('form/f_p_f.html',Datos = session)
    else:
        flash("No has enviado un registro")
        return render_template('form/f_p_f.html',Datos = session)
  except:
    flash("Llena todos los Campos Correctamente")
    return render_template('form/f_p_f.html',Datos = session)


@app.route('/r_a_p_xd',methods=['POST'])
def registro_actalizacion_planning_cross():
  try:
    if request.method == 'POST':
        id = request.form['id']
        marchamo =  request.form['marchamo']
        marchamo2 =  request.form['marchamo2']
        estatus = 'Enviado'
        usuario = session['FullName']
        now = datetime.now()
        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE planing
        SET hora_de_despacho = %s,
        marchamo = %s,
        marchamo2 = %s,
        status = %s
        WHERE id_planing  = %s
        """,(now,marchamo,marchamo2,estatus,id))
        mysql.connection.commit()
        flash("Registro Exitoso")
        return render_template('form/f_p_xd.html',Datos = session)
    else:
        flash("No has enviado un registro")
        return render_template('form/f_p_xd.html',Datos = session)
  except:
    flash("Llena todos los Campos Correctamente")
    return render_template('form/f_p_xd.html',Datos = session)


@app.route('/r_a_o_np',methods=['POST'])
def registro_actalizacion_ordenes_no_procesables():
  # try:
    if request.method == 'POST':
        id_orden =  request.form['id_orden']
        estatus = request.form['Status']
        usuario = session['FullName']
        Comentario = request.form['Comentario']
        now = datetime.now()
        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE ordenes_no_procesables
        SET estatus_orden = %s,
        Comentario = %s,
        fecha_actualizacion = %s,
        responsable_actualizacion = %s
        WHERE id_orden  = %s
        """,(estatus,Comentario,now,usuario,id_orden))
        mysql.connection.commit()
        flash("Registro Exitoso")
        return render_template('form/f_a_o.html',Datos = session)
    else:
        flash("No has enviado un registro")
        return render_template('form/f_a_o.html',Datos = session)
  # except:
  #   flash("Llena todos los Campos Correctamente")
  #   return render_template('form/f_a_o.html',Datos = session)

#Cerrar Session
@app.route('/logout')
def Cerrar_session():
  session.clear()
  return render_template('index.html')


@app.route('/t_e_s/<rowi>',methods=['POST','GET'])
def Reporte_entradas_service(rowi):
  try:
      if request.method == 'POST':
        if request.method == 'GET':
          session['rowi']=rowi
          row1 = int(session['rowi_t_e_s'])
          row2 = 100
        else:
            row1 = int(session['rowi_t_e_s'])
            row2 =100
        if 'valor' in request.form:
          if len(request.form['valor'])>0:
            session['filtro_t_e_s']=request.form['filtro']
            session['valor_t_e_s']=request.form['valor']
            if len(request.form['inicio'])>0:
              session['inicio_t_e_s']=request.form['inicio']
              if len(request.form['fin'])>0:
                session['fin_t_e_s']=request.form['fin']
                cur = mysql.connection.cursor()
                cur.execute('SELECT * FROM entrada_svcs WHERE {} LIKE \'%{}%\' AND Fecha_Creación	 BETWEEN \'{}\' AND \'{}\' LIMIT {}, {}'.format(session['filtro_t_e_s'],session['valor_t_e_s'],session['inicio_t_e_s'],session['fin_t_e_s'],row1,row2))
                data = cur.fetchall()
                return render_template('reportes/t_e_s.html',Datos = session,Infos =data)
              else:
                cur = mysql.connection.cursor()
                cur.execute('SELECT * FROM entrada_svcs WHERE {} LIKE \'%{}%\' AND Fecha_Creación	 = \'{}\'  LIMIT {}, {}'.format(session['filtro_t_e_s'],session['valor_t_e_s'],session['inicio_t_e_s'],row1,row2))
                data = cur.fetchall()
                return render_template('reportes/t_e_s.html',Datos = session,Infos =data)
            else:
              cur = mysql.connection.cursor()
              cur.execute('SELECT * FROM entrada_svcs WHERE {} LIKE \'%{}%\' LIMIT {}, {}'.format(session['filtro_t_e_s'],session['valor_t_e_s'],row1,row2))
              data = cur.fetchall()
              return render_template('reportes/t_e_s.html',Datos = session,Infos =data)
          else:
            cur = mysql.connection.cursor()
            cur.execute('SELECT * FROM entrada_svcs LIMIT {}, {}'.format(row1,row2))
            data = cur.fetchall()
            return render_template('reportes/t_e_s.html',Datos = session,Infos =data) 
        else:
          cur = mysql.connection.cursor()
          cur.execute('SELECT * FROM entrada_svcs LIMIT {}, {}'.format(row1,row2))
          data = cur.fetchall()
          return render_template('reportes/t_e_s.html',Datos = session,Infos =data)
      else: 
        if request.method == 'GET':
          session['rowi_t_e_s']=rowi
          row1 = int(session['rowi_t_e_s'])
          row2 = 50
        else:
          row1 = int(session['rowi_t_e_s'])
          row2 =50
        if 'valor_t_e_s' in session:
          if len(session['valor_t_e_s'])>0:
            if 'inicio_t_e_s' in session:
              if len(session['inicio_t_e_s'])>0:
                if 'fin_t_e_s' in session:
                  if len(session['fin_t_e_s'])>0:
                    cur = mysql.connection.cursor()
                    cur.execute('SELECT * FROM entrada_svcs WHERE {} LIKE \'%{}%\' AND Fecha_Creación BETWEEN \'{}\' AND \'{}\' LIMIT {}, {}'.format(session['filtro_t_e_s'],session['valor_t_e_s'],session['inicio_t_e_s'],session['fin_t_e_s'],row1,row2))
                    data = cur.fetchall()
                    return render_template('reportes/t_e_s.html',Datos = session,Infos =data)
                  else:
                    cur = mysql.connection.cursor()
                    cur.execute('SELECT * FROM entrada_svcs WHERE {} LIKE \'%{}%\' AND Fecha_Creación = \'{}\'  LIMIT {}, {}'.format(session['filtro_t_e_s'],session['valor_t_e_s'],session['inicio_t_e_s'],row1,row2))
                    data = cur.fetchall()
                    return render_template('reportes/t_e_s.html',Datos = session,Infos =data)
                else:
                    cur = mysql.connection.cursor()
                    cur.execute('SELECT * FROM entrada_svcs WHERE {} LIKE \'%{}%\' AND Fecha_Creación = \'{}\'  LIMIT {}, {}'.format(session['filtro_t_e_s'],session['valor_t_e_s'],session['inicio_t_e_s'],row1,row2))
                    data = cur.fetchall()
                    return render_template('reportes/t_e_s.html',Datos = session,Infos =data)
              else:
                cur = mysql.connection.cursor()
                cur.execute('SELECT * FROM entrada_svcs WHERE {} LIKE \'%{}%\' LIMIT {}, {}'.format(session['filtro_t_e_s'],session['valor_t_e_s'],row1,row2))
                data = cur.fetchall()
                return render_template('reportes/t_e_s.html',Datos = session,Infos =data)  
            else:
              cur = mysql.connection.cursor()
              cur.execute('SELECT * FROM entrada_svcs WHERE {} LIKE \'%{}%\' LIMIT {}, {}'.format(session['filtro_t_e_s'],session['valor_t_e_s'],row1,row2))
              data = cur.fetchall()
              return render_template('reportes/t_e_s.html',Datos = session,Infos =data)
          else:
            cur = mysql.connection.cursor()
            cur.execute('SELECT * FROM entrada_svcs LIMIT {}, {}'.format(row1,row2))
            data = cur.fetchall()
            return render_template('reportes/t_e_s.html',Datos = session,Infos =data)
        else:
          cur = mysql.connection.cursor()
          cur.execute('SELECT * FROM entrada_svcs LIMIT {}, {}'.format(row1,row2))
          data = cur.fetchall()
          return render_template('reportes/t_e_s.html',Datos = session,Infos =data)
          
  except:
    flash("Inicia Secion")
    return render_template('index.html')


@app.route('/t_n_p/<rowi>',methods=['POST','GET'])
def Reporte_ordenes_no_procesables(rowi):
  try:
      if request.method == 'POST':
        if request.method == 'GET':
          session['rowi_t_n_p']=rowi
          row1 = int(session['rowi_t_n_p'])
          row2 = 100
        else:
            row1 = int(session['rowi_t_n_p'])
            row2 =100
        if 'valor' in request.form:
          if len(request.form['valor'])>0:
            session['filtro_t_n_p']=request.form['filtro']
            session['valor_t_n_p']=request.form['valor']
            if len(request.form['inicio'])>0:
              session['inicio_t_n_p']=request.form['inicio']
              if len(request.form['fin'])>0:
                session['fin_t_n_p']=request.form['fin']
                cur = mysql.connection.cursor()
                cur.execute('SELECT * FROM ordenes_no_procesables WHERE {} LIKE \'%{}%\' AND fecha BETWEEN \'{}\' AND \'{}\' LIMIT {}, {}'.format(session['filtro_t_n_p'],session['valor_t_n_p'],session['inicio_t_n_p'],session['fin_t_n_p'],row1,row2))
                data = cur.fetchall()
                return render_template('reportes/t_n_p.html',Datos = session,Infos =data)
              else:
                cur = mysql.connection.cursor()
                cur.execute('SELECT * FROM ordenes_no_procesables WHERE {} LIKE \'%{}%\' AND fecha = \'{}\'  LIMIT {}, {}'.format(session['filtro_t_n_p'],session['valor_t_n_p'],session['inicio_t_n_p'],row1,row2))
                data = cur.fetchall()
                return render_template('reportes/t_n_p.html',Datos = session,Infos =data)
            else:
              cur = mysql.connection.cursor()
              cur.execute('SELECT * FROM ordenes_no_procesables WHERE {} LIKE \'%{}%\' LIMIT {}, {}'.format(session['filtro_t_n_p'],session['valor_t_n_p'],row1,row2))
              data = cur.fetchall()
              return render_template('reportes/t_n_p.html',Datos = session,Infos =data)
          else:
            cur = mysql.connection.cursor()
            cur.execute('SELECT * FROM ordenes_no_procesables LIMIT {}, {}'.format(row1,row2))
            data = cur.fetchall()
            return render_template('reportes/t_n_p.html',Datos = session,Infos =data) 
        else:
          cur = mysql.connection.cursor()
          cur.execute('SELECT * FROM ordenes_no_procesables LIMIT {}, {}'.format(row1,row2))
          data = cur.fetchall()
          return render_template('reportes/t_n_p.html',Datos = session,Infos =data)
        
      else: 
        if request.method == 'GET':
          session['rowi_t_n_p']=rowi
          row1 = int(session['rowi_t_n_p'])
          row2 = 50
        else:
          row1 = int(session['rowi_t_n_p'])
          row2 =50
        if 'valor_t_n_p' in session:
          if len(session['valor_t_n_p'])>0:
            if 'inicio_t_n_p' in session:
              if len(session['inicio_t_n_p'])>0:
                if 'fin_t_n_p' in session:
                  if len(session['fin_t_n_p'])>0:
                    cur = mysql.connection.cursor()
                    cur.execute('SELECT * FROM ordenes_no_procesables WHERE {} LIKE \'%{}%\' AND dia BETWEEN \'{}\' AND \'{}\' LIMIT {}, {}'.format(session['filtro_t_n_p'],session['valor_t_n_p'],session['inicio_t_n_p'],session['fin_t_n_p'],row1,row2))
                    data = cur.fetchall()
                    return render_template('reportes/t_n_p.html',Datos = session,Infos =data)
                  else:
                    cur = mysql.connection.cursor()
                    cur.execute('SELECT * FROM ordenes_no_procesables WHERE {} LIKE \'%{}%\' AND dia = \'{}\'  LIMIT {}, {}'.format(session['filtro_t_n_p'],session['valor_t_n_p'],session['inicio_t_n_p'],row1,row2))
                    data = cur.fetchall()
                    return render_template('reportes/t_n_p.html',Datos = session,Infos =data)
                else:
                    cur = mysql.connection.cursor()
                    cur.execute('SELECT * FROM ordenes_no_procesables WHERE {} LIKE \'%{}%\' AND dia = \'{}\'  LIMIT {}, {}'.format(session['filtro_t_n_p'],session['valor_t_n_p'],session['inicio_t_n_p'],row1,row2))
                    data = cur.fetchall()
                    return render_template('reportes/t_n_p.html',Datos = session,Infos =data)
              else:
                cur = mysql.connection.cursor()
                cur.execute('SELECT * FROM ordenes_no_procesables WHERE {} LIKE \'%{}%\' LIMIT {}, {}'.format(session['filtro_t_n_p'],session['valor_t_n_p'],row1,row2))
                data = cur.fetchall()
                return render_template('reportes/t_n_p.html',Datos = session,Infos =data)  
            else:
              cur = mysql.connection.cursor()
              cur.execute('SELECT * FROM ordenes_no_procesables WHERE {} LIKE \'%{}%\' LIMIT {}, {}'.format(session['filtro_t_n_p'],session['valor_t_n_p'],row1,row2))
              data = cur.fetchall()
              return render_template('reportes/t_n_p.html',Datos = session,Infos =data)
          else:
            cur = mysql.connection.cursor()
            cur.execute('SELECT * FROM ordenes_no_procesables LIMIT {}, {}'.format(row1,row2))
            data = cur.fetchall()
            return render_template('reportes/t_n_p.html',Datos = session,Infos =data)
        else:
          cur = mysql.connection.cursor()
          cur.execute('SELECT * FROM ordenes_no_procesables LIMIT {}, {}'.format(row1,row2))
          data = cur.fetchall()
          return render_template('reportes/t_n_p.html',Datos = session,Infos =data)
  except:
    flash("Inicia Secion")
    return render_template('index.html')


@app.route('/t_p/<rowi>',methods=['POST','GET'])
def Reporte_prealert(rowi):
  try:
      if request.method == 'POST':
        if request.method == 'GET':
          session['rowi_t_p']=rowi
          row1 = int(session['rowi_t_p'])
          row2 = 50
        else:
            row1 = int(session['rowi_t_p'])
            row2 =50
        if 'valor' in request.form:
          if len(request.form['valor'])>0:
            session['filtro_t_p']=request.form['filtro']
            session['valor_t_p']=request.form['valor']
            if 'datefilter' in request.form:
              if len(request.form['datefilter'])>0:
                daterangef=request.form['datefilter']
                daterange=daterangef.replace("-", "' AND '")
                session['datefilter']=daterange
                cur = mysql.connection.cursor()
                cur.execute('SELECT * FROM prealert WHERE {} LIKE \'%{}%\' AND Fecha BETWEEN \'{}\'  LIMIT {}, {}'.format(session['filtro_t_p'],session['valor_t_p'],session['datefilter'],row1,row2))
                data = cur.fetchall()
                return render_template('reportes/t_p.html',Datos = session,Infos =data)
              else:
                cur = mysql.connection.cursor()
                cur.execute('SELECT * FROM prealert WHERE {} LIKE \'%{}%\'  LIMIT {}, {}'.format(session['filtro_t_p'],session['valor_t_p'],row1,row2))
                data = cur.fetchall()
                return render_template('reportes/t_p.html',Datos = session,Infos =data)
            else:
              session.pop('datefilter')
              cur = mysql.connection.cursor()
              cur.execute('SELECT * FROM prealert WHERE {} LIKE \'%{}%\'  LIMIT {}, {}'.format(session['filtro_t_p'],session['valor_t_p'],row1,row2))
              data = cur.fetchall()
              return render_template('reportes/t_p.html',Datos = session,Infos =data)
          else:
            if 'datefilter' in request.form:
              if len(request.form['datefilter'])>0:
                if 'valor_t_p' in session:
                  if len(session['valor_t_p'])>0:
                    daterangef=request.form['datefilter']
                    daterange=daterangef.replace("-", "' AND '")
                    session['datefilter']=daterange
                    cur = mysql.connection.cursor()
                    cur.execute('SELECT * FROM prealert WHERE {} LIKE \'%{}%\' AND Fecha BETWEEN \'{}\'  LIMIT {}, {}'.format(session['filtro_t_p'],session['valor_t_p'],session['datefilter'],row1,row2))
                    data = cur.fetchall()
                    return render_template('reportes/t_p.html',Datos = session,Infos =data)
                  else:
                    session.pop('filtro_t_p')
                    session.pop('valor_t_p')
                    cur = mysql.connection.cursor()
                    cur.execute('SELECT * FROM prealert WHERE Fecha BETWEEN \'{}\'  LIMIT {}, {}'.format(session['datefilter'],row1,row2))
                    data = cur.fetchall()
                    return render_template('reportes/t_p.html',Datos = session,Infos =data)
                else:
                  cur = mysql.connection.cursor()
                  cur.execute('SELECT * FROM prealert WHERE Fecha BETWEEN \'{}\'  LIMIT {}, {}'.format(session['datefilter'],row1,row2))
                  data = cur.fetchall()
                  return render_template('reportes/t_p.html',Datos = session,Infos =data)
              else:
                if 'valor_t_p' in session:
                  session.pop('filtro_t_p')
                  session.pop('valor_t_p')
                  if 'datefilter' in session:
                    session.pop('datefilter')
                  cur = mysql.connection.cursor()
                  cur.execute('SELECT * FROM prealert  LIMIT {}, {}'.format(row1,row2))
                  data = cur.fetchall()
                  return render_template('reportes/t_p.html',Datos = session,Infos =data)
                else:
                  cur = mysql.connection.cursor()
                  cur.execute('SELECT * FROM prealert  LIMIT {}, {}'.format(row1,row2))
                  data = cur.fetchall()
                  return render_template('reportes/t_p.html',Datos = session,Infos =data)
            else:
              if 'valor_t_p' in session:
                if 'datefilter' in session:
                    session.pop('datefilter')
                session.pop('filtro_t_p')
                session.pop('valor_t_p')
                cur = mysql.connection.cursor()
                cur.execute('SELECT * FROM prealert  LIMIT {}, {}'.format(row1,row2))
                data = cur.fetchall()
                return render_template('reportes/t_p.html',Datos = session,Infos =data)
              else:
                cur = mysql.connection.cursor()
                cur.execute('SELECT * FROM prealert  LIMIT {}, {}'.format(row1,row2))
                data = cur.fetchall()
                return render_template('reportes/t_p.html',Datos = session,Infos =data)

        else:
          if 'valor_t_p' in session:
            if len(session['valor_t_p'])>0:
              if 'datefilter' in session:
                if len(session['datefilter'])>0:
                  cur = mysql.connection.cursor()
                  cur.execute('SELECT * FROM prealert WHERE {} LIKE \'%{}%\' AND Fecha BETWEEN \'{}\'  LIMIT {}, {}'.format(session['filtro_t_p'],session['valor_t_p'],session['datefilter'],row1,row2))
                  data = cur.fetchall()
                  return render_template('reportes/t_p.html',Datos = session,Infos =data)
                else:
                  session.pop('datefilter')
                  cur = mysql.connection.cursor()
                  cur.execute('SELECT * FROM prealert WHERE {} LIKE \'%{}%\'  LIMIT {}, {}'.format(session['filtro_t_p'],session['valor_t_p'],row1,row2))
                  data = cur.fetchall()
                  return render_template('reportes/t_p.html',Datos = session,Infos =data)
              else:
                cur = mysql.connection.cursor()
                cur.execute('SELECT * FROM prealert WHERE {} LIKE \'%{}%\'  LIMIT {}, {}'.format(session['filtro_t_p'],session['valor_t_p'],row1,row2))
                data = cur.fetchall()
                return render_template('reportes/t_p.html',Datos = session,Infos =data) 
            else:
              session.pop('filtro_t_p')
              session.pop('valor_t_p')
              if 'datefilter' in session:
                if len(session['datefilter'])>0:
                  cur = mysql.connection.cursor()
                  cur.execute('SELECT * FROM prealert WHERE Fecha BETWEEN \'{}\'  LIMIT {}, {}'.format(session['datefilter'],row1,row2))
                  data = cur.fetchall()
                  return render_template('reportes/t_p.html',Datos = session,Infos =data)
                else:
                  cur = mysql.connection.cursor()
                  cur.execute('SELECT * FROM prealert LIMIT {}, {}'.format(row1,row2))
                  data = cur.fetchall()
                  return render_template('reportes/t_p.html',Datos = session,Infos =data)
              else:
                cur = mysql.connection.cursor()
                cur.execute('SELECT * FROM prealert  LIMIT {}, {}'.format(row1,row2))
                data = cur.fetchall()
                return render_template('reportes/t_p.html',Datos = session,Infos =data)
          else:
            if 'datefilter' in session:
              if len(session['datefilter'])>0:
                cur = mysql.connection.cursor()
                cur.execute('SELECT * FROM prealert WHERE Fecha BETWEEN \'{}\'  LIMIT {}, {}'.format(session['datefilter'],row1,row2))
                data = cur.fetchall()
                return render_template('reportes/t_p.html',Datos = session,Infos =data)
              else:
                session.pop('datefilter')
                cur = mysql.connection.cursor()
                cur.execute('SELECT * FROM prealert LIMIT {}, {}'.format(row1,row2))
                data = cur.fetchall()
                return render_template('reportes/t_p.html',Datos = session,Infos =data)
            else:
              if 'datefilter' in request.form:
                if len(request.form['datefilter'])>0:
                  daterangef=request.form['datefilter']
                  daterange=daterangef.replace("-", "' AND '")
                  session['datefilter']=daterange
                  cur = mysql.connection.cursor()
                  cur.execute('SELECT * FROM prealert WHERE  Fecha BETWEEN \'{}\'  LIMIT {}, {}'.format(session['datefilter'],row1,row2))
                  data = cur.fetchall()
                  return render_template('reportes/t_p.html',Datos = session,Infos =data)
                else:
                  cur = mysql.connection.cursor()
                  cur.execute('SELECT * FROM prealert LIMIT {}, {}'.format(row1,row2))
                  data = cur.fetchall()
                  return render_template('reportes/t_p.html',Datos = session,Infos =data) 
              else:
                cur = mysql.connection.cursor()
                cur.execute('SELECT * FROM prealert LIMIT {}, {}'.format(row1,row2))
                data = cur.fetchall()
                return render_template('reportes/t_p.html',Datos = session,Infos =data) 
      else: 
        if request.method == 'GET':
          session['rowi_t_p']=rowi
          row1 = int(session['rowi_t_p'])
          row2 = 50
        else:
          row1 = int(session['rowi_t_p'])
          row2 =50
        if 'valor_t_p' in session:
          if len(session['valor_t_p'])>0:
            if 'datefilter' in session:
              if len(session['datefilter'])>0:
                cur = mysql.connection.cursor()
                cur.execute('SELECT * FROM prealert WHERE {} LIKE \'%{}%\' AND Fecha BETWEEN \'{}\'  LIMIT {}, {}'.format(session['filtro_t_p'],session['valor_t_p'],session['datefilter'],row1,row2))
                data = cur.fetchall()
                return render_template('reportes/t_p.html',Datos = session,Infos =data)
              else:
                session.pop('datefilter')
                cur = mysql.connection.cursor()
                cur.execute('SELECT * FROM prealert WHERE {} LIKE \'%{}%\'  LIMIT {}, {}'.format(session['filtro_t_p'],session['valor_t_p'],row1,row2))
                data = cur.fetchall()
                return render_template('reportes/t_p.html',Datos = session,Infos =data)
            else:
              cur = mysql.connection.cursor()
              cur.execute('SELECT * FROM prealert WHERE {} LIKE \'%{}%\'  LIMIT {}, {}'.format(session['filtro_t_p'],session['valor_t_p'],row1,row2))
              data = cur.fetchall()
              return render_template('reportes/t_p.html',Datos = session,Infos =data) 
          else:
            session.pop('filtro_t_p')
            session.pop('valor_t_p')
            if 'datefilter' in session:
              if len(session['datefilter'])>0:
                cur = mysql.connection.cursor()
                cur.execute('SELECT * FROM prealert WHERE Fecha BETWEEN \'{}\'  LIMIT {}, {}'.format(session['datefilter'],row1,row2))
                data = cur.fetchall()
                return render_template('reportes/t_p.html',Datos = session,Infos =data)
              else:
                session.pop('datefilter')
                cur = mysql.connection.cursor()
                cur.execute('SELECT * FROM prealert LIMIT {}, {}'.format(row1,row2))
                data = cur.fetchall()
                return render_template('reportes/t_p.html',Datos = session,Infos =data)
            else:
              cur = mysql.connection.cursor()
              cur.execute('SELECT * FROM prealert  LIMIT {}, {}'.format(row1,row2))
              data = cur.fetchall()
              return render_template('reportes/t_p.html',Datos = session,Infos =data)
        else:
          if 'datefilter' in session:
            if len(session['datefilter'])>0:
              cur = mysql.connection.cursor()
              cur.execute('SELECT * FROM prealert WHERE Fecha BETWEEN \'{}\'  LIMIT {}, {}'.format(session['datefilter'],row1,row2))
              data = cur.fetchall()
              return render_template('reportes/t_p.html',Datos = session,Infos =data)
            else:
              session.pop('datefilter')
              cur = mysql.connection.cursor()
              cur.execute('SELECT * FROM prealert LIMIT {}, {}'.format(row1,row2))
              data = cur.fetchall()
              return render_template('reportes/t_p.html',Datos = session,Infos =data)
          else:
            cur = mysql.connection.cursor()
            cur.execute('SELECT * FROM prealert  LIMIT {}, {}'.format(row1,row2))
            data = cur.fetchall()
            return render_template('reportes/t_p.html',Datos = session,Infos =data)         
  except:
    flash("Inicia Secion")
    return render_template('index.html')


@app.route('/t_planning/<rowi>',methods=['POST','GET'])
def Reporte_planning(rowi):
  try:
      if request.method == 'POST':
        if request.method == 'GET':
          session['rowi_t_planning']=rowi
          row1 = int(session['rowi_t_planning'])
          row2 = 100
        else:
            row1 = int(session['rowi_t_planning'])
            row2 =100
        if 'valor' in request.form:
          if len(request.form['valor'])>0:
            session['filtro_t_planning']=request.form['filtro']
            session['valor_t_planning']=request.form['valor']
            if len(request.form['inicio'])>0:
              session['inicio_t_planning']=request.form['inicio']
              if len(request.form['fin'])>0:
                session['fin_t_planning']=request.form['fin']
                cur = mysql.connection.cursor()
                cur.execute('SELECT * FROM planing WHERE {} LIKE \'%{}%\' AND Fecha_Creación	 BETWEEN \'{}\' AND \'{}\' LIMIT {}, {}'.format(session['filtro_t_planning'],session['valor_t_planning'],session['inicio_t_planning'],session['fin_t_planning'],row1,row2))
                data = cur.fetchall()
                return render_template('reportes/t_planning.html',Datos = session,Infos =data)
              else:
                cur = mysql.connection.cursor()
                cur.execute('SELECT * FROM planing WHERE {} LIKE \'%{}%\' AND Fecha_Creación	 = \'{}\'  LIMIT {}, {}'.format(session['filtro_t_planning'],session['valor_t_planning'],session['inicio_t_planning'],row1,row2))
                data = cur.fetchall()
                return render_template('reportes/t_planning.html',Datos = session,Infos =data)
            else:
              cur = mysql.connection.cursor()
              cur.execute('SELECT * FROM planing WHERE {} LIKE \'%{}%\' LIMIT {}, {}'.format(session['filtro_t_planning'],session['valor_t_planning'],row1,row2))
              data = cur.fetchall()
              return render_template('reportes/t_planning.html',Datos = session,Infos =data)
          else:
            cur = mysql.connection.cursor()
            cur.execute('SELECT * FROM planing LIMIT {}, {}'.format(row1,row2))
            data = cur.fetchall()
            return render_template('reportes/t_planning.html',Datos = session,Infos =data) 
        else:
          cur = mysql.connection.cursor()
          cur.execute('SELECT * FROM planing LIMIT {}, {}'.format(row1,row2))
          data = cur.fetchall()
          return render_template('reportes/t_planning.html',Datos = session,Infos =data)
      else: 
        if request.method == 'GET':
          session['rowi_t_planning']=rowi
          row1 = int(session['rowi_t_planning'])
          row2 = 50
        else:
          row1 = int(session['rowi_t_planning'])
          row2 =50
        if 'valor_t_planning' in session:
          if len(session['valor_t_planning'])>0:
            if 'inicio_t_planning' in session:
              if len(session['inicio_t_planning'])>0:
                if 'fin_t_planning' in session:
                  if len(session['fin_t_planning'])>0:
                    cur = mysql.connection.cursor()
                    cur.execute('SELECT * FROM planing WHERE {} LIKE \'%{}%\' AND Fecha_agendada BETWEEN \'{}\' AND \'{}\' LIMIT {}, {}'.format(session['filtro_t_planning'],session['valor_t_planning'],session['inicio_t_planning'],session['fin_t_planning'],row1,row2))
                    data = cur.fetchall()
                    return render_template('reportes/t_planning.html',Datos = session,Infos =data)
                  else:
                    cur = mysql.connection.cursor()
                    cur.execute('SELECT * FROM planing WHERE {} LIKE \'%{}%\' AND Fecha_agendada = \'{}\'  LIMIT {}, {}'.format(session['filtro_t_planning'],session['valor_t_planning'],session['inicio_t_planning'],row1,row2))
                    data = cur.fetchall()
                    return render_template('reportes/t_planning.html',Datos = session,Infos =data)
                else:
                    cur = mysql.connection.cursor()
                    cur.execute('SELECT * FROM planing WHERE {} LIKE \'%{}%\' AND Fecha_agendada = \'{}\'  LIMIT {}, {}'.format(session['filtro_t_planning'],session['valor_t_planning'],session['inicio_t_planning'],row1,row2))
                    data = cur.fetchall()
                    return render_template('reportes/t_planning.html',Datos = session,Infos =data)
              else:
                cur = mysql.connection.cursor()
                cur.execute('SELECT * FROM planing WHERE {} LIKE \'%{}%\' LIMIT {}, {}'.format(session['filtro_t_planning'],session['valor_t_planning'],row1,row2))
                data = cur.fetchall()
                return render_template('reportes/t_planning.html',Datos = session,Infos =data)  
            else:
              cur = mysql.connection.cursor()
              cur.execute('SELECT * FROM planing WHERE {} LIKE \'%{}%\' LIMIT {}, {}'.format(session['filtro_t_planning'],session['valor_t_planning'],row1,row2))
              data = cur.fetchall()
              return render_template('reportes/t_planning.html',Datos = session,Infos =data)
          else:
            cur = mysql.connection.cursor()
            cur.execute('SELECT * FROM planing LIMIT {}, {}'.format(row1,row2))
            data = cur.fetchall()
            return render_template('reportes/t_planning.html',Datos = session,Infos =data)
        else:
          cur = mysql.connection.cursor()
          cur.execute('SELECT * FROM planing LIMIT {}, {}'.format(row1,row2))
          data = cur.fetchall()
          return render_template('reportes/t_planning.html',Datos = session,Infos =data)
  except:
    flash("Inicia Secion")
    return render_template('index.html')


@app.route('/t_r_f/<rowi>',methods=['POST','GET'])
def Reporte_recibo_full(rowi):
  try:
      if request.method == 'POST':
        if request.method == 'GET':
          session['rowi_t_r_f']=rowi
          row1 = int(session['rowi_t_r_f'])
          row2 = 100
        else:
            row1 = int(session['rowi_t_r_f'])
            row2 =100
        if 'valor' in request.form:
          if len(request.form['valor'])>0:
            session['filtro_t_r_f']=request.form['filtro']
            session['valor_t_r_f']=request.form['valor']
            if len(request.form['inicio'])>0:
              session['inicio_t_r_f']=request.form['inicio']
              if len(request.form['fin'])>0:
                session['fin_t_r_f']=request.form['fin']
                cur = mysql.connection.cursor()
                cur.execute('SELECT * FROM recibo_fc WHERE {} LIKE \'%{}%\' AND dia BETWEEN \'{}\' AND \'{}\' LIMIT {}, {}'.format(session['filtro_t_r_f'],session['valor_t_r_f'],session['inicio_t_r_f'],session['fin_t_r_f'],row1,row2))
                data = cur.fetchall()
                return render_template('reportes/t_r_f.html',Datos = session,Infos =data)
              else:
                cur = mysql.connection.cursor()
                cur.execute('SELECT * FROM recibo_fc WHERE {} LIKE \'%{}%\' AND dia = \'{}\'  LIMIT {}, {}'.format(session['filtro_t_r_f'],session['valor_t_r_f'],session['inicio_t_r_f'],row1,row2))
                data = cur.fetchall()
                return render_template('reportes/t_r_f.html',Datos = session,Infos =data)
            else:
              cur = mysql.connection.cursor()
              cur.execute('SELECT * FROM recibo_fc WHERE {} LIKE \'%{}%\' LIMIT {}, {}'.format(session['filtro_t_r_f'],session['valor_t_r_f'],row1,row2))
              data = cur.fetchall()
              return render_template('reportes/t_r_f.html',Datos = session,Infos =data)
          else:
            cur = mysql.connection.cursor()
            cur.execute('SELECT * FROM recibo_fc LIMIT {}, {}'.format(row1,row2))
            data = cur.fetchall()
            return render_template('reportes/t_r_f.html',Datos = session,Infos =data) 
        else:
          cur = mysql.connection.cursor()
          cur.execute('SELECT * FROM recibo_fc LIMIT {}, {}'.format(row1,row2))
          data = cur.fetchall()
          return render_template('reportes/t_r_f.html',Datos = session,Infos =data)
      else: 
        if request.method == 'GET':
          session['rowi_t_r_f']=rowi
          row1 = int(session['rowi_t_r_f'])
          row2 = 50
        else:
          row1 = int(session['rowi_t_r_f'])
          row2 =50
        if 'valor_t_r_f' in session:
          if len(session['valor_t_r_f'])>0:
            if 'inicio_t_r_f' in session:
              if len(session['inicio_t_r_f'])>0:
                if 'fin_t_r_f' in session:
                  if len(session['fin_t_r_f'])>0:
                    cur = mysql.connection.cursor()
                    cur.execute('SELECT * FROM recibo_fc WHERE {} LIKE \'%{}%\' AND dia BETWEEN \'{}\' AND \'{}\' LIMIT {}, {}'.format(session['filtro_t_r_f'],session['valor_t_r_f'],session['inicio_t_r_f'],session['fin_t_r_f'],row1,row2))
                    data = cur.fetchall()
                    return render_template('reportes/t_r_f.html',Datos = session,Infos =data)
                  else:
                    cur = mysql.connection.cursor()
                    cur.execute('SELECT * FROM recibo_fc WHERE {} LIKE \'%{}%\' AND dia = \'{}\'  LIMIT {}, {}'.format(session['filtro_t_r_f'],session['valor_t_r_f'],session['inicio_t_r_f'],row1,row2))
                    data = cur.fetchall()
                    return render_template('reportes/t_r_f.html',Datos = session,Infos =data)
                else:
                    cur = mysql.connection.cursor()
                    cur.execute('SELECT * FROM recibo_fc WHERE {} LIKE \'%{}%\' AND dia = \'{}\'  LIMIT {}, {}'.format(session['filtro_t_r_f'],session['valor_t_r_f'],session['inicio_t_r_f'],row1,row2))
                    data = cur.fetchall()
                    return render_template('reportes/t_r_f.html',Datos = session,Infos =data)
              else:
                cur = mysql.connection.cursor()
                cur.execute('SELECT * FROM recibo_fc WHERE {} LIKE \'%{}%\' LIMIT {}, {}'.format(session['filtro_t_r_f'],session['valor_t_r_f'],row1,row2))
                data = cur.fetchall()
                return render_template('reportes/t_r_f.html',Datos = session,Infos =data)  
            else:
              cur = mysql.connection.cursor()
              cur.execute('SELECT * FROM recibo_fc WHERE {} LIKE \'%{}%\' LIMIT {}, {}'.format(session['filtro_t_r_f'],session['valor_t_r_f'],row1,row2))
              data = cur.fetchall()
              return render_template('reportes/t_r_f.html',Datos = session,Infos =data)
          else:
            cur = mysql.connection.cursor()
            cur.execute('SELECT * FROM recibo_fc LIMIT {}, {}'.format(row1,row2))
            data = cur.fetchall()
            return render_template('reportes/t_r_f.html',Datos = session,Infos =data)
        else:
          cur = mysql.connection.cursor()
          cur.execute('SELECT * FROM recibo_fc LIMIT {}, {}'.format(row1,row2))
          data = cur.fetchall()
          return render_template('reportes/t_r_f.html',Datos = session,Infos =data)
  except:
    flash("Inicia Secion")
    return render_template('index.html')


@app.route('/t_s_s/<rowi>',methods=['POST','GET'])
def Reporte_salida_service(rowi):
  try:
      if request.method == 'POST':
        if request.method == 'GET':
          session['rowi_t_s_s']=rowi
          row1 = int(session['rowi_t_s_s'])
          row2 = 100
        else:
            row1 = int(session['rowi_t_s_s'])
            row2 =100
        if 'valor' in request.form:
          if len(request.form['valor'])>0:
            session['filtro_t_s_s']=request.form['filtro']
            session['valor_t_s_s']=request.form['valor']
            if len(request.form['inicio'])>0:
              session['inicio_t_s_s']=request.form['inicio']
              if len(request.form['fin'])>0:
                session['fin_t_s_s']=request.form['fin']
                cur = mysql.connection.cursor()
                cur.execute('SELECT * FROM salida_svcs WHERE {} LIKE \'%{}%\' AND Fecha_Creación	 BETWEEN \'{}\' AND \'{}\' LIMIT {}, {}'.format(session['filtro_t_s_s'],session['valor_t_s_s'],session['inicio_t_s_s'],session['fin_t_s_s'],row1,row2))
                data = cur.fetchall()
                return render_template('reportes/t_s_s.html',Datos = session,Infos =data)
              else:
                cur = mysql.connection.cursor()
                cur.execute('SELECT * FROM salida_svcs WHERE {} LIKE \'%{}%\' AND Fecha_Creación	 = \'{}\'  LIMIT {}, {}'.format(session['filtro_t_s_s'],session['valor_t_s_s'],session['inicio_t_s_s'],row1,row2))
                data = cur.fetchall()
                return render_template('reportes/t_s_s.html',Datos = session,Infos =data)
            else:
              cur = mysql.connection.cursor()
              cur.execute('SELECT * FROM salida_svcs WHERE {} LIKE \'%{}%\' LIMIT {}, {}'.format(session['filtro_t_s_s'],session['valor_t_s_s'],row1,row2))
              data = cur.fetchall()
              return render_template('reportes/t_s_s.html',Datos = session,Infos =data)
          else:
            cur = mysql.connection.cursor()
            cur.execute('SELECT * FROM salida_svcs LIMIT {}, {}'.format(row1,row2))
            data = cur.fetchall()
            return render_template('reportes/t_s_s.html',Datos = session,Infos =data) 
        else:
          cur = mysql.connection.cursor()
          cur.execute('SELECT * FROM salida_svcs LIMIT {}, {}'.format(row1,row2))
          data = cur.fetchall()
          return render_template('reportes/t_s_s.html',Datos = session,Infos =data)
        
      else: 
        if request.method == 'GET':
          session['rowi_t_s_s']=rowi
          row1 = int(session['rowi_t_s_s'])
          row2 = 50
        else:
          row1 = int(session['rowi_t_s_s'])
          row2 =50
        if 'valor_t_s_s' in session:
          if len(session['valor_t_s_s'])>0:
            if 'inicio_t_s_s' in session:
              if len(session['inicio_t_s_s'])>0:
                if 'fin_t_s_s' in session:
                  if len(session['fin_t_s_s'])>0:
                    cur = mysql.connection.cursor()
                    cur.execute('SELECT * FROM salida_svcs WHERE {} LIKE \'%{}%\' AND Fecha_Creación BETWEEN \'{}\' AND \'{}\' LIMIT {}, {}'.format(session['filtro_t_s_s'],session['valor_t_s_s'],session['inicio_t_s_s'],session['fin_t_s_s'],row1,row2))
                    data = cur.fetchall()
                    return render_template('reportes/t_s_s.html',Datos = session,Infos =data)
                  else:
                    cur = mysql.connection.cursor()
                    cur.execute('SELECT * FROM salida_svcs WHERE {} LIKE \'%{}%\' AND Fecha_Creación = \'{}\'  LIMIT {}, {}'.format(session['filtro_t_s_s'],session['valor_t_s_s'],session['inicio_t_s_s'],row1,row2))
                    data = cur.fetchall()
                    return render_template('reportes/t_s_s.html',Datos = session,Infos =data)
                else:
                    cur = mysql.connection.cursor()
                    cur.execute('SELECT * FROM salida_svcs WHERE {} LIKE \'%{}%\' AND Fecha_Creación = \'{}\'  LIMIT {}, {}'.format(session['filtro_t_s_s'],session['valor_t_s_s'],session['inicio_t_s_s'],row1,row2))
                    data = cur.fetchall()
                    return render_template('reportes/t_s_s.html',Datos = session,Infos =data)
              else:
                cur = mysql.connection.cursor()
                cur.execute('SELECT * FROM salida_svcs WHERE {} LIKE \'%{}%\' LIMIT {}, {}'.format(session['filtro_t_s_s'],session['valor_t_s_s'],row1,row2))
                data = cur.fetchall()
                return render_template('reportes/t_s_s.html',Datos = session,Infos =data)  
            else:
              cur = mysql.connection.cursor()
              cur.execute('SELECT * FROM salida_svcs WHERE {} LIKE \'%{}%\' LIMIT {}, {}'.format(session['filtro_t_s_s'],session['valor_t_s_s'],row1,row2))
              data = cur.fetchall()
              return render_template('reportes/t_s_s.html',Datos = session,Infos =data)
          else:
            cur = mysql.connection.cursor()
            cur.execute('SELECT * FROM salida_svcs LIMIT {}, {}'.format(row1,row2))
            data = cur.fetchall()
            return render_template('reportes/t_s_s.html',Datos = session,Infos =data)
        else:
          cur = mysql.connection.cursor()
          cur.execute('SELECT * FROM salida_svcs LIMIT {}, {}'.format(row1,row2))
          data = cur.fetchall()
          return render_template('reportes/t_s_s.html',Datos = session,Infos =data)
  except:
    flash("Inicia Secion")
    return render_template('index.html')


@app.route('/validacion_recibo',methods=['Post'])
def Verificacion_orden_recibo():
  try:
      if request.method == 'POST':
        session['key_pa'] = request.form['prealertkey']
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM prealert WHERE  ID_Envio_Prealert = \'{}\' limit 1'.format(session['key_pa']))
        data = cur.fetchall()
        if len(data)>0:
          return render_template('form/f_recibo.html',Datos = session,Info = data)
        else:
          flash("Numero de Orden Invalido")
          return render_template('form/f_r_f.html',Datos = session)
      else:
        flash("No has enviado un registro")
        return render_template('form/f_r_f.html',Datos = session)
  except:
    flash("Llena todos los Campos Correctamente")
    return render_template('home.html',Datos = session)


@app.route('/registro_recibo',methods=['POST'])
def registroRecibo():
  try:
      if request.method == 'POST':
        key_pa = session['key_pa']
        facility = session['FcName']
        siteName = session['SiteName']
        Orden = request.form['Orden']
        Paquetera = request.form['Paquetera']
        status = request.form['status']
        comentario = request.form['comentario']
        reponsable = session['FullName']
        now = datetime.now()
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO recibo_fc (ID_Envio_Prealert, Orden, Paquetera, status, Comentario, Facility, SiteName, Responsable, Fecha, Fecha_Hora) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(key_pa, Orden, Paquetera, status, comentario, facility, siteName, reponsable, now, now))
        mysql.connection.commit() 
        flash("Registro Exitoso")
        return render_template('form/f_recibo.html',Datos = session)
      else:
        flash("No has enviado un registro")
        return render_template('form/f_r_f.html',Datos = session)
  except:
    flash("Llena todos los Campos Correctamente")
    return render_template('form/f_r_f.html',Datos = session)


@app.route('/pdf',methods=['POST','GET'])
def pdf_template():
  
        Key =  session['key_pa']
        img =qrcode.make(Key)
        file =open('qr.png','wb')
        img.save(file)
        lugar = 'De: '+session['FcName']+' | '+session['SiteName']
        facility = session['FcName']
        site = session['SiteName']
        today= datetime.today()
        if 'destinoPrealert' in session:
          cur = mysql.connection.cursor()
          cur.execute('SELECT * FROM prealert WHERE ID_Envio_Prealert = \'{}\' AND Origen =\'{}\' AND SiteName =\'{}\'  '.format(Key,facility,site))
          result = cur.fetchall()
          if len(result)>0:
            Marchamo = " Marchamo:  "+ str(result[0][11])
            Destino = ' a: '+str(result[0][4])+' | '+str(result[0][5])
            EmpresaTransporte = " Empresa Transporte: "+str(result[0][6]) 
            Transportista = "  Transportista: " + str(result[0][7])
            Placas = "  Placas: "+ str(result[0][8]).upper()
        else:
          cur = mysql.connection.cursor()
          cur.execute('SELECT * FROM prealert WHERE ID_Envio_Prealert = \'{}\' AND Origen =\'{}\' AND SiteName =\'{}\'  '.format(Key,facility,site))
          result = cur.fetchall()
 
        pdf = FPDF(orientation = 'P',unit = 'mm', format='A4')
        pdf.add_page()
         
        page_width = pdf.w - 2 * pdf.l_margin
         
        pdf.ln(5)
        pdf.image('static/img/MercadoLibre_logo.png', x= 20, y = 10, w=50, h = 20)
        pdf.set_font('Times','B',30)
        pdf.set_text_color(0,47,109)  
        pdf.text(x = 80, y = 19 ,txt =  "Receiving Log. Inversa" )
        pdf.text(x = 80, y = 29 ,txt =  "Paquetes e Insumo" )
        pdf.ln(80)
        
        pdf.image('qr.png', x= 20, y = 45, w=40, h = 40)

        pdf.set_font('Times','B',12) 
        
        pdf.set_text_color(0,0,0) 
        pdf.text( x= 70, y = 57, txt = str(today))
        pdf.text( x= 70, y = 67, txt = "Pre-Alert Key:")
        pdf.text( x= 70, y = 77, txt = Key)

        col_widt3 = page_width/2


        pdf.set_font('Times','B',12) 
        pdf.cell(col_widt3, 0.0, lugar, align='C')
        if 'destinoPrealert' in session:
          
          if len(result)>0:
            pdf.cell(col_widt3, 0.0, Destino, align='C')
         
        pdf.ln(10)

        if 'destinoPrealert' in session:
          
          if len(result)>0:
            pdf.set_font('Times','B',12) 
            pdf.cell(page_width, 0.0, EmpresaTransporte, align='C')
            pdf.ln(10)

            pdf.set_font('Times','B',12) 
            pdf.cell(page_width, 0.0, Transportista, align='C')
            pdf.ln(10)

            pdf.set_font('Times','B',12) 
            pdf.cell(page_width, 0.0, Placas, align='C')
            pdf.ln(10)


        pdf.set_font('Times', 'B', 12)
        col_widt2 = page_width/3
        col_widt1 = page_width/3
        col_width = page_width/3
        
        
        th = pdf.font_size
         
        pdf.cell(col_widt2, th,"ID", align='C')
        pdf.cell(col_width, th,"Orden",align='C')
        pdf.cell(col_width, th, "Paquetera", align='C')
        pdf.ln(th)


        pdf.set_font('Times', '', 12)
        col_widt2 = page_width/3
        col_widt1 = page_width/3
        col_width = page_width/3
         
        th = pdf.font_size
         
        for row in result:
            pdf.cell(col_widt2, th, str(row[0]), align='C')
            pdf.cell(col_width, th, str(row[9]), align='C')
            pdf.cell(col_width, th, row[10], align='C')
            pdf.ln(th)
         
        pdf.ln(10)
        if 'destinoPrealert' in session:
          
          if len(result)>0:
            pdf.set_font('Times','B',12)
            pdf.cell(page_width, 8.0, Marchamo, align='C')
          
        pdf.ln(15)
        pdf.set_font('Times','B',12)
        pdf.cell(page_width, 8.0, '_______________________________________________________________________', align='C')
         
        return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf', headers={'Content-Disposition':'Atachment;filename=Prealert'+Key+'.pdf'})


@app.route("/FinalizarRecibo",methods=['POST','GET'])
def finalizarRecibo():
  try:
    if 'FullName' in session:
      cur = mysql.connection.cursor()
      cur.execute('SELECT count(Orden) FROM prealert WHERE  ID_Envio_Prealert = \'{}\' And Origen = \'Cross Dock\''.format(session['key_pa']))
      numOrdenCross = cur.fetchall()
      cur = mysql.connection.cursor()
      cur.execute('SELECT count(Orden) FROM recibo_fc WHERE  ID_Envio_Prealert = \'{}\' '.format(session['key_pa']))
      numOrdenFull = cur.fetchall()
      result = numOrdenCross[0][0]-numOrdenFull[0][0]
      if result>0:
        return render_template("actualizacion/confirmacion.html", Datos =session, faltante= result)
      else:
        flash("Recibo Finalizado")
        return render_template("form/f_r_f.html", Datos =session)
  except:  
    return render_template("home.html",Datos=session)


@app.route("/trackinOrden",methods=['POST','GET'])
def Track_Inorden():
  try:
    if 'FullName' in session:
        return render_template("form/trackinorden.html", Datos =session)
  except:  
    return render_template("home.html",Datos=session)


@app.route("/trackinPrealert",methods=['POST','GET'])
def Track_In():
  try:
    if 'FullName' in session:
        return render_template("form/trackinprealert.html", Datos =session)
  except:  
    return render_template("home.html",Datos=session)


@app.route("/Trackin_ordenes",methods=['POST','GET'])
def Track_in_ordenes():
  # try:
    if 'FullName' in session:
      Orden= request.form['Orden']
      cur = mysql.connection.cursor()
      cur.execute('SELECT * FROM prealert WHERE  Orden = {} And Origen = \'Service Center\''.format(Orden))
      Servicedata = cur.fetchall()
      cur = mysql.connection.cursor()
      cur.execute('SELECT * FROM recibo_fc WHERE  Orden = {} And Facility = \'Cross Dock\''.format(Orden))
      reciboCrossdata = cur.fetchall()
      cur.execute('SELECT * FROM prealert WHERE  Orden = {} And Origen = \'Cross Dock\''.format(Orden))
      Crossdata = cur.fetchall()
      cur = mysql.connection.cursor()
      cur.execute('SELECT * FROM recibo_fc WHERE  Orden = {} And Facility = \'Fullfilment\' '.format(Orden))
      Fulldata = cur.fetchall()
      return render_template("actualizacion/trackin_ordenes.html", Datos =session,Servicedata = Servicedata,Crossdata=Crossdata,Fulldata=Fulldata,Orden=Orden,reciboCrossdata=reciboCrossdata)
  # except:  
  #   return render_template("form/trackinorden.html",Datos=session)


@app.route("/Trackin_prealetkey",methods=['POST','GET'])
def Track_in_prealert():
  # try:
    if 'FullName' in session:
      key= request.form['prealertkey']
      cur = mysql.connection.cursor()
      cur.execute('SELECT * FROM prealert WHERE  ID_Envio_Prealert = \'{}\' And Origen = \'Service Center\''.format(key))
      Servicedata = cur.fetchall()
      cur = mysql.connection.cursor()
      cur.execute('SELECT * FROM prealert WHERE  ID_Envio_Prealert = \'{}\' And Origen = \'Cross Dock\''.format(key))
      Crossdata = cur.fetchall()
      cur = mysql.connection.cursor()
      cur.execute('SELECT * FROM recibo_fc WHERE  ID_Envio_Prealert = \'{}\' '.format(key))
      Fulldata = cur.fetchall()
      return render_template("actualizacion/trackin_prealert.html", Datos =session,Servicedata = Servicedata,Crossdata=Crossdata,Fulldata=Fulldata)
  # except:  
  #   return render_template("form/trackin.html",Datos=session)


@app.route('/csvPrealert',methods=['POST','GET'])
def crear_csvPrealert():
    site=session['SiteName']
    row1 = int(session['rowi_t_p'])
    row2 =50
    if 'valor_t_p' in session:
      if len(session['valor_t_p'])>0:
        if 'datefilter' in session:
          if len(session['datefilter'])>0:
            cur = mysql.connection.cursor()
            cur.execute('SELECT * FROM prealert WHERE {} LIKE \'%{}%\' AND Fecha BETWEEN \'{}\'  LIMIT {}, {}'.format(session['filtro_t_p'],session['valor_t_p'],session['datefilter'],row1,row2))
            data = cur.fetchall()
          else:
            cur = mysql.connection.cursor()
            cur.execute('SELECT * FROM prealert WHERE {} LIKE \'%{}%\'  LIMIT {}, {}'.format(session['filtro_t_p'],session['valor_t_p'],row1,row2))
            data = cur.fetchall()
        else:
          cur = mysql.connection.cursor()
          cur.execute('SELECT * FROM prealert WHERE {} LIKE \'%{}%\'  LIMIT {}, {}'.format(session['filtro_t_p'],session['valor_t_p'],row1,row2))
          data = cur.fetchall()
      else:
        if 'datefilter' in session:
          if len(session['datefilter'])>0:
            cur = mysql.connection.cursor()
            cur.execute('SELECT * FROM prealert WHERE Fecha BETWEEN \'{}\'  LIMIT {}, {}'.format(session['datefilter'],row1,row2))
            data = cur.fetchall()
          else:
            cur = mysql.connection.cursor()
            cur.execute('SELECT * FROM prealert LIMIT {}, {}'.format(row1,row2))
            data = cur.fetchall()
        else:
          cur = mysql.connection.cursor()
          cur.execute('SELECT * FROM prealert  LIMIT {}, {}'.format(row1,row2))
          data = cur.fetchall()
    else:
      if 'datefilter' in session:
        if len(session['datefilter'])>0:
          cur = mysql.connection.cursor()
          cur.execute('SELECT * FROM prealert WHERE Fecha BETWEEN \'{}\'  LIMIT {}, {}'.format(session['datefilter'],row1,row2))
          data = cur.fetchall()
        else:
          cur = mysql.connection.cursor()
          cur.execute('SELECT * FROM prealert LIMIT {}, {}'.format(row1,row2))
      else:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM prealert  LIMIT {}, {}'.format(row1,row2))
        data = cur.fetchall()
    datos="Id"+","+"Pre-Alert key"+","+"Facility Origen"+","+"Site Origen"+","+"Facility Destino"+","+"Site Destino"+","+"Transporte"+","+"Transportista"+","+"Placas"+","+"Orden"+","+"Paquetera"+","+"Marchamo"+","+"Responsable"+","+"Fecha y Hora"+","+"\n"
    for res in data:
      datos+=str(res[0])
      datos+=","+str(res[1])
      datos+=","+str(res[2])
      datos+=","+str(res[3])
      datos+=","+str(res[4])
      datos+=","+str(res[5])
      datos+=","+str(res[6])
      datos+=","+str(res[7])
      datos+=","+str(res[8])
      datos+=","+str(res[9])
      datos+=","+str(res[10])
      datos+=","+str(res[11])
      datos+=","+str(res[12])
      datos+=","+str(res[14])
      datos+="\n"

    print(datos)
    response = make_response(datos)
    response.headers["Content-Disposition"] = "attachment; filename="+"Prealert"+str(datetime.today())+".csv"
    return response

@app.route('/insumos',methods=['GET'])
def insumos():
  if 'FullName' in session:
    return render_template('insumos.html',Datos = session)
  else:
    flash("Inicia Sesion")
    return render_template('index.html')



@app.route('/paquetes',methods=['GET'])
def paquetes():
  if 'FullName' in session:
    return render_template('paquetes.html',Datos = session)
  else:
    flash("Inicia Sesion")
    return render_template('index.html')


@app.route('/gestiondepaquetes',methods=['GET'])
def gestiondepaquetes():
  if 'FullName' in session:
    return render_template('gestiondepaquetes.html',Datos = session)
  else:
    flash("Inicia Sesion")
    return render_template('index.html')

@app.route('/comercialcarrier',methods=['GET'])
def comercialcarrier():
  if 'FullName' in session:
    return render_template('comercialcarrier.html',Datos = session)
  else:
    flash("Inicia Sesion")
    return render_template('index.html')

@app.route('/logistic',methods=['GET'])
def logistic():
  if 'FullName' in session:
    return render_template('logistic.html',Datos = session)
  else:
    flash("Inicia Sesion")
    return render_template('index.html')





if __name__=='__main__':
    app.run(port = 3000, debug =True)