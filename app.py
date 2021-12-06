from flask import Flask, render_template, request, redirect, url_for, flash, session, make_response 
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date
import hashlib

app = Flask(__name__)

#MySQL Connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'isumos'
mysql = MySQL(app)

# settings
app.secret_key = 'mysecretkey'

#Direccion Principal 
@app.route('/')
def Index():
  try:
    if session['FullName'] != None:
      return redirect('/form')
    else:
      return render_template('index.html')
  except:
    return render_template('index.html')

#Valida el Acceso a la Plataforma 
@app.route('/validar', methods=['POST'])
def validar():
    if request.method == 'POST':
      usuario =  request.form['user']
      password = request.form['password']
      cur = mysql.connection.cursor()
      cur.execute('SELECT * FROM usuarios WHERE Usuario = \'{}\' LIMIT 1 '.format(usuario))
      data = cur.fetchall()
      if len(data) > 0 :
          if check_password_hash(data[0][5],password):
            session['FullName'] = data[0][1]
            session['UserName'] = data[0][2]
            session['FcName'] = data[0][3]
            session['SiteName'] = data[0][4]
            session['Rango'] = data[0][6]
            return redirect('/form')
          else:
            flash('Contraseña Incorrecta')
            return render_template('index.html')
      else:
        flash('Usuario Incorrecto')
        return render_template('index.html')    

#Formularios de Registro Entradas Y Salidas 
@app.route('/form',methods=['POST','GET'])
def form():
  try:
    if session['FullName'] != None:
      if request.method == 'POST':
        if session['Rango'] == 'Administrador':
          session['FcName']= request.form['centro_de_Trabajo']
          session['Formulario']= request.form['formulario']
          return render_template('form.html',Datos = session)
        else:
          session['Formulario']= request.form['formulario']
          return render_template('form.html',Datos = session)
      else:
        session['Formulario']= None
        return render_template('form.html',Datos = session)
    else:
      flash("Inicia Secion")
      return render_template('index.html')
  except:
    flash("Inicia Secion")
    return render_template('index.html')

#Redirigie a el Formulario de Registro de Usuarios 
@app.route('/registro')
def registro():
  try:
    if session['FullName'] != None:
      if session['Rango'] == 'Administrador':

        return render_template('registro.html', Datos = session)
      else:
        flash("Acseso Denegado")
      return render_template('index.html')
    else:
      flash("Inicia Secion")
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
            return render_template('registro.html')
          else:
            cur = mysql.connection.cursor()
            cur.execute('INSERT INTO `usuarios` (Nombre, Usuario, ltrabajo, cdt, contraseña, Rango) VALUES (%s,%s,%s,%s,%s,%s)',(nombre,usuario,ltrabajo,cdt,password,rango))
            mysql.connection.commit()
            flash("Registro Correcto")
            return render_template('registro.html')
        else:
          flash("Las Contraceñas no Cionciden")
          return render_template('registro.html')
  except:
    flash("Llena todos los Campos Correctamente")
    return render_template('registro.html')
def _create_password(password):
   return generate_password_hash(password,'pbkdf2:sha256:30',30)

#Registros de Formularios 
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
        return render_template('form.html',Datos = session)
      else:
        flash("No has enviado un registro")
        return render_template('form.html',Datos = session)
  except:
    flash("Llena todos los Campos Correctamente")
    return render_template('form.html',Datos = session)

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
        return render_template('form.html',Datos = session)
      else:
        flash("No has enviado un registro")
        return render_template('form.html',Datos = session)
  except:
    flash("Llena todos los Campos Correctamente")
    return render_template('form.html',Datos = session)

# Registro de Salidas Service Center
@app.route('/registro_prealert',methods=['POST'])
def registro_prealert():
  try:
      if request.method == 'POST':
        fc =  session['FcName']
        cdt =  session['SiteName']
        id_de_envio = request.form['id_de_envio']
        Codificación =  request.form['Codificación']
        Metodo = request.form['Metodo']
        Facility =  request.form['Facility']
        Transporte = request.form['Transporte']
        Trasportista =  request.form['Trasportista']
        Placas = request.form['Placas']
        Sello = request.form['Sello']
        usuario =  session['FullName']
        now = datetime.now()
        
        if len(Trasportista)>0 and len(Placas)>0 and len(Sello)>0:
          cur = mysql.connection.cursor()
          cur.execute('INSERT INTO prealert (responsable, lugaDeTrabajo, cdt, id_de_envio, Codificación, Metodo, Facility, Transporte	, Trasportista, Placas, Sello, dia, fecha) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(usuario,fc,cdt,id_de_envio,Codificación,Metodo,Facility,Transporte,Trasportista,Placas,Sello,now,now))
          mysql.connection.commit() 
          flash("Registro Exitoso")
          return render_template('form.html',Datos = session)
        else:
          flash("Llenan todoos los Campos ")
          return render_template('form.html',Datos = session)
      else:
        flash("No has enviado un registro")
        return render_template('form.html',Datos = session)
  except:
    flash("Llena todos los Campos Correctamente")
    return render_template('form.html',Datos = session)


@app.route('/registro_fcs_entrada',methods=['POST'])
def registro_fcs_e():
  try:
      if request.method == 'POST':
        cdt =  session['SiteName']
        Pallets_en_buen_estado =  request.form['Pallets_en_buen_estado']
        Pallets_en_mal_estado = request.form['Pallets_en_mal_estado']
        Pallets_Totales_Recibidos = int(Pallets_en_buen_estado)+int(Pallets_en_mal_estado)
        Gaylords_en_buen_estado = request.form['Gaylords_en_buen_estado']
        Gaylords_en_mal_estado =  request.form['Gaylords_en_mal_estado']
        Gaylords_Totales_Recibidos =  int(Gaylords_en_buen_estado)+int(Gaylords_en_mal_estado)
        cajas = request.form['cajas']
        costales =  request.form['costales']
        Centro_de_trabajo_origen = request.form['Centro_de_trabajo_origen']
        Cross_Dock_origen =  request.form['Cross_Dock_origen']
        Service_Center_Origen = request.form['Service_Center_Origen']
        usuario =  session['FullName']
        now = datetime.now()
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO entrada_fc (Fulfillment, Pallets_Totales_Recibidos, Pallets_en_buen_estado, Pallets_en_mal_estado, Gaylords_Totales_Recibidos, Gaylords_en_buen_estado, Gaylords_en_mal_estado, Cajas, Costales, Centro_de_trabajo_origen, Cross_Dock_origen, Service_Center_Origen, Responsable, Fecha_Creación, Fecha_Hora) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(cdt,Pallets_Totales_Recibidos,Pallets_en_buen_estado,Pallets_en_mal_estado,Gaylords_Totales_Recibidos,Gaylords_en_buen_estado,Gaylords_en_mal_estado,cajas,costales,Centro_de_trabajo_origen,Cross_Dock_origen,Service_Center_Origen,usuario,now,now))
        mysql.connection.commit() 
        flash("Registro Exitoso")
        return render_template('form.html',Datos = session)
      else:
        flash("No has enviado un registro")
        return render_template('form.html',Datos = session)
  except:
    flash("Llena todos los Campos Correctamente")
    return render_template('form.html',Datos = session)


@app.route('/registro_fcs_salida',methods=['POST'])
def registro_fcs_s():
  try:
      if request.method == 'POST':
        cdt =  session['SiteName']
        Tarimas_enviadas = request.form['Tarimas_enviadas']
        Gaylord_Enviados =  request.form['Gaylord_Enviados']
        cajas = request.form['cajas']
        costales =  request.form['costales']
        centro_de_trabajo_Destino = request.form['centro_de_trabajo_Destino']
        Service_Center =  request.form['Service_Center']
        fc_Destino = request.form['FC_Destino']
        usuario =  session['FullName']
        now = datetime.now()
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO salida_fc (Fulfillment, Tarimas_enviadas, Gaylord_Enviados, cajas, costales, centro_de_trabajo_Destino, Service_Center, FC_Destino, Responsable, Fecha_Creación, Fecha_Hora) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(cdt,Tarimas_enviadas,Gaylord_Enviados,cajas,costales,centro_de_trabajo_Destino,Service_Center,fc_Destino,usuario,now,now))
        mysql.connection.commit() 
        flash("Registro Exitoso")
        return render_template('form.html',Datos = session)
      else:
        flash("No has enviado un registro")
        return render_template('form.html',Datos = session)
  except:
    flash("Llena todos los Campos Correctamente")
    return render_template('form.html',Datos = session)


@app.route('/registro_fcs_tranfer',methods=['POST'])
def registro_fcs_t():
  try:
      if request.method == 'POST':
        cdt =  session['SiteName']
        Pallets = request.form['Pallets']
        Fulfillment_origen =  request.form['Fulfillment_origen']
        usuario =  session['FullName']
        now = datetime.now()
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO entrada_tranferencias_fc (Fulfillment, Pallets, Fulfillment_origen, Responsable, Fecha_Creación, Fecha_Hora) VALUES (%s,%s,%s,%s,%s,%s)',(cdt,Pallets,Fulfillment_origen,usuario,now,now))
        mysql.connection.commit() 
        flash("Registro Exitoso")
        return render_template('form.html',Datos = session)
      else:
        flash("No has enviado un registro")
        return render_template('form.html',Datos = session)
  except:
    flash("Llena todos los Campos Correctamente")
    return render_template('form.html',Datos = session)


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
        return render_template('form.html',Datos = session)
      else:
        flash("No has enviado un registro")
        return render_template('form.html',Datos = session)
  except:
    flash("Llena todos los Campos Correctamente")
    return render_template('form.html',Datos = session)


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
          return render_template('form.html',Datos = session)
        else:
          flash("Llena Todos Los Datos")
          return render_template('form.html',Datos = session)
      else:
        flash("No has enviado un registro")
        return render_template('form.html',Datos = session)
  except:
        flash("No has enviado un registro")
        return render_template('form.html',Datos = session)


@app.route('/registro_xd_entrada',methods=['POST'])
def registro_xd_entrada():
  try:
      if request.method == 'POST':
        cdt = session['SiteName']
        Tarima_en_buen_estado = request.form['Tarima_en_buen_estado']
        Tarimas_en_mal_estado = request.form['Tarimas_en_mal_estado']
        Total_tarimas = int(Tarima_en_buen_estado)+int(Tarimas_en_mal_estado)
        Gaylors_en_buen_estado = request.form['Gaylors_en_buen_estado']
        Gaylors_en_mal_estado = request.form['Gaylors_en_mal_estado']
        Total_Gaylors = int(Gaylors_en_buen_estado)+int(Gaylors_en_mal_estado)
        Cajas = request.form['cajas']
        Costales = request.form['costales']
        Destino_Proveniente = request.form['Destino_Proveniente']
        usuario = session['FullName']
        now = datetime.now()
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO entrada_xd (Centro_de_trabajo_donde_te_encuentras, Total_tarimas, Tarima_en_buen_estado, Tarimas_en_mal_estado, Total_Gaylors, Gaylors_en_buen_estado, Gaylors_en_mal_estado, cajas, Costales, Destino_Proveniente, Responsable, Fecha_Creación, Fecha_Hora) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(cdt,Total_tarimas,Tarima_en_buen_estado,Tarimas_en_mal_estado,Total_Gaylors,Gaylors_en_buen_estado,Gaylors_en_mal_estado,Cajas,Costales,Destino_Proveniente,usuario,now,now))
        mysql.connection.commit() 
        flash("Registro Exitoso")
        return render_template('form.html',Datos = session)
      else:
        flash("No has enviado un registro")
        return render_template('form.html',Datos = session)
  except:
    flash("Llena todos los Campos Correctamente")
    return render_template('form.html',Datos = session)


@app.route('/registro_xd_salida',methods=['POST'])
def registro_xd_s():
  try:
      if request.method == 'POST':
        cdt = session['SiteName']
        Tarimas_Enviadas = request.form['Tarimas_Enviadas']
        Gaylord_Enviados = request.form['Gaylord_Enviados']
        cajas = request.form['cajas']
        costales = request.form['costales']
        Destino_de_la_carga = request.form['Destino_de_la_carga']
        Service_Center = request.form['Service_Center']
        Fulfillment = request.form['Fulfillment']
        usuario = session['FullName']
        now = datetime.now()
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO salida_xd (Centro_de_trabajo_donde_te_encuentras, Tarimas_Enviadas, Gaylord_Enviados, cajas, costales, Destino_de_la_carga, service_center, Fulfillment, Responsable, Fecha_Creación, Fecha_Hora) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(cdt,Tarimas_Enviadas,Gaylord_Enviados,cajas,costales,Destino_de_la_carga,Service_Center,Fulfillment,usuario,now,now))
        mysql.connection.commit() 
        flash("Registro Exitoso")
        return render_template('form.html',Datos = session)
      else:
        flash("No has enviado un registro")
        return render_template('form.html',Datos = session)
  except:
    flash("Llena todos los Campos Correctamente")
    return render_template('form.html',Datos = session)


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
        return render_template('form.html',Datos = session)
      else:
        flash("No has enviado un registro")
        return render_template('form.html',Datos = session)
  except:
    flash("Llena todos los Campos Correctamente")
    return render_template('form.html',Datos = session)


@app.route('/a_formularios',methods=['POST'])
def a_form():
  try:
      if request.method == 'POST':
        if session['FcName']=='Cross Dock' and session['Formulario']=='planning':
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
            return render_template('actualizacion.html',Datos = session,Info = data)
          else:
            flash("ID Invalido")
            return render_template('form.html',Datos = session)
        elif session['FcName']=='Fullfilment' and session['Formulario']=='planning':
          id_planing = request.form['id_planing']
          cur = mysql.connection.cursor()
          cur.execute('SELECT * FROM planing WHERE id_planing = \'{}\' LIMIT 1 '.format(id_planing))
          data = cur.fetchall()
          if len(data)>0:
            return render_template('actualizacion.html',Datos = session,Info = data)
          else:
            flash("ID Invalido")
            return render_template('form.html',Datos = session)
        elif session['FcName']=='Fullfilment' and session['Formulario']=='f_a_estatus':
          orden = request.form['orden']
          status = 'Pendiente'
          cur = mysql.connection.cursor()
          cur.execute('SELECT * FROM ordenes_no_procesables WHERE orden = \'{}\' AND estatus_orden = \'{}\' LIMIT 1 '.format(orden,status))
          data = cur.fetchall()
          if len(data)>0:
            return render_template('actualizacion.html',Datos = session,Info = data)
          else:
            flash("Numero de Orden Invalido")
            return render_template('form.html',Datos = session)
      else:
        flash("No has enviado un registro")
        return render_template('form.html',Datos = session)
  except:
    flash("Llena todos los Campos Correctamente")
    return render_template('form.html',Datos = session)


@app.route('/actualizar',methods=['POST'])
def actualizacion():
  try:
    if request.method == 'POST':
      if session['FcName']=='Cross Dock' and session['Formulario'] =='planning':
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
        return render_template('form.html',Datos = session)
      elif session['FcName']=='Fullfilment' and session['Formulario'] =='planning':
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
        return render_template('form.html',Datos = session)
      elif session['FcName']=='Fullfilment' and session['Formulario'] =='f_a_estatus':
        id_orden =  request.form['id_orden']
        estatus = 'Cerrado'
        usuario = session['FullName']
        now = datetime.now()
        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE ordenes_no_procesables
        SET estatus_orden = %s,
        fecha_actualizacion = %s,
        responsable_actualizacion = %s
        WHERE id_orden  = %s
        """,(estatus,now,usuario,id_orden))
        mysql.connection.commit()
        flash("Registro Exitoso")
        return render_template('form.html',Datos = session)
    else:
        flash("No has enviado un registro")
        return render_template('form.html',Datos = session)
  except:
    flash("Llena todos los Campos Correctamente")
    return render_template('form.html',Datos = session)


@app.route('/logout')
def logout():
  session.clear()
  flash("Sesion Finalizada")
  return render_template('index.html')


@app.route('/Reportes/<rowi>',methods=['POST','GET'],)
def Reporte(rowi):
  # try:
      if request.method == 'POST':
        if session['Rango'] == 'Administrador':
          if 'centro_de_Trabajo' in request.form:
            session['FcName']= request.form['centro_de_Trabajo']
            session['tabla']= request.form['tabla']
        if 'tabla' in request.form:  
          session['tabla']= request.form['tabla']

        if request.method == 'GET':
          session['rowi']=rowi
          row1 = int(session['rowi'])
          row2 = 100
        else:
            row1 = int(session['rowi'])
            row2 =100

        # Inicio de Tabla Entradas Fulfilment    
        if  session['FcName'] == 'Fullfilment' and session['tabla'] =='Entrada':
          if 'valor' in request.form:
            if len(request.form['valor'])>0:
              session['filtro']=request.form['filtro']
              session['valor']=request.form['valor']
              if len(request.form['inicio'])>0:
                session['inicio']=request.form['inicio']
                if len(request.form['fin'])>0:
                  session['fin']=request.form['fin']
                  cur = mysql.connection.cursor()
                  cur.execute('SELECT * FROM entrada_fc WHERE {} LIKE \'%{}%\' AND Fecha_Creación BETWEEN \'{}\' AND \'{}\' LIMIT {}, {}'.format(session['filtro'],session['valor'],session['inicio'],session['fin'],row1,row2))
                  data = cur.fetchall()
                  return render_template('reportes.html',Datos = session,Infos =data)
                else:
                  cur = mysql.connection.cursor()
                  cur.execute('SELECT * FROM entrada_fc WHERE {} LIKE \'%{}%\' AND Fecha_Creación = \'{}\'  LIMIT {}, {}'.format(session['filtro'],session['valor'],session['inicio'],row1,row2))
                  data = cur.fetchall()
                  return render_template('reportes.html',Datos = session,Infos =data)
              else:
                cur = mysql.connection.cursor()
                cur.execute('SELECT * FROM entrada_fc WHERE {} LIKE \'%{}%\' LIMIT {}, {}'.format(session['filtro'],session['valor'],row1,row2))
                data = cur.fetchall()
                return render_template('reportes.html',Datos = session,Infos =data)
            else:
              cur = mysql.connection.cursor()
              cur.execute('SELECT * FROM entrada_fc LIMIT {}, {}'.format(row1,row2))
              data = cur.fetchall()
              return render_template('reportes.html',Datos = session,Infos =data) 
          else:
            cur = mysql.connection.cursor()
            cur.execute('SELECT * FROM entrada_fc LIMIT {}, {}'.format(row1,row2))
            data = cur.fetchall()
            return render_template('reportes.html',Datos = session,Infos =data)
        # Inicio de Tabla SalidaS Fulfilment        
        elif  session['FcName'] == 'Fullfilment' and session['tabla'] =='Salida':
          if 'valor' in request.form:
            if len(request.form['valor'])>0:
              session['filtro']=request.form['filtro']
              session['valor']=request.form['valor']
              if len(request.form['inicio'])>0:
                session['inicio']=request.form['inicio']
                if len(request.form['fin'])>0:
                  session['fin']=request.form['fin']
                  cur = mysql.connection.cursor()
                  cur.execute('SELECT * FROM salida_fc WHERE {} LIKE \'%{}%\' AND Fecha_Creación BETWEEN \'{}\' AND \'{}\' LIMIT {}, {}'.format(session['filtro'],session['valor'],session['inicio'],session['fin'],row1,row2))
                  data = cur.fetchall()
                  return render_template('reportes.html',Datos = session,Infos =data)
                else:
                  cur = mysql.connection.cursor()
                  cur.execute('SELECT * FROM salida_fc WHERE {} LIKE \'%{}%\' AND Fecha_Creación = \'{}\'  LIMIT {}, {}'.format(session['filtro'],session['valor'],session['inicio'],row1,row2))
                  data = cur.fetchall()
                  return render_template('reportes.html',Datos = session,Infos =data)
              else:
                cur = mysql.connection.cursor()
                cur.execute('SELECT * FROM salida_fc WHERE {} LIKE \'%{}%\' LIMIT {}, {}'.format(session['filtro'],session['valor'],row1,row2))
                data = cur.fetchall()
                return render_template('reportes.html',Datos = session,Infos =data)
            else:
              cur = mysql.connection.cursor()
              cur.execute('SELECT * FROM salida_fc LIMIT {}, {}'.format(row1,row2))
              data = cur.fetchall()
              return render_template('reportes.html',Datos = session,Infos =data) 
          else:
            cur = mysql.connection.cursor()
            cur.execute('SELECT * FROM salida_fc LIMIT {}, {}'.format(row1,row2))
            data = cur.fetchall()
            return render_template('reportes.html',Datos = session,Infos =data)
        # Inicio de Tabla Transfer Fulfilment 
        elif  session['FcName'] == 'Fullfilment' and session['tabla'] =='Entrada_Tranferencias':
          if 'valor' in request.form:
            if len(request.form['valor'])>0:
              session['filtro']=request.form['filtro']
              session['valor']=request.form['valor']
              if len(request.form['inicio'])>0:
                session['inicio']=request.form['inicio']
                if len(request.form['fin'])>0:
                  session['fin']=request.form['fin']
                  cur = mysql.connection.cursor()
                  cur.execute('SELECT * FROM entrada_tranferencias_fc WHERE {} LIKE \'%{}%\' AND Fecha_Creación BETWEEN \'{}\' AND \'{}\' LIMIT {}, {}'.format(session['filtro'],session['valor'],session['inicio'],session['fin'],row1,row2))
                  data = cur.fetchall()
                  return render_template('reportes.html',Datos = session,Infos =data)
                else:
                  cur = mysql.connection.cursor()
                  cur.execute('SELECT * FROM entrada_tranferencias_fc WHERE {} LIKE \'%{}%\' AND Fecha_Creación = \'{}\'  LIMIT {}, {}'.format(session['filtro'],session['valor'],session['inicio'],row1,row2))
                  data = cur.fetchall()
                  return render_template('reportes.html',Datos = session,Infos =data)
              else:
                cur = mysql.connection.cursor()
                cur.execute('SELECT * FROM entrada_tranferencias_fc WHERE {} LIKE \'%{}%\' LIMIT {}, {}'.format(session['filtro'],session['valor'],row1,row2))
                data = cur.fetchall()
                return render_template('reportes.html',Datos = session,Infos =data)
            else:
              cur = mysql.connection.cursor()
              cur.execute('SELECT * FROM entrada_tranferencias_fc LIMIT {}, {}'.format(row1,row2))
              data = cur.fetchall()
              return render_template('reportes.html',Datos = session,Infos =data) 
          else:
            cur = mysql.connection.cursor()
            cur.execute('SELECT * FROM entrada_tranferencias_fc LIMIT {}, {}'.format(row1,row2))
            data = cur.fetchall()
            return render_template('reportes.html',Datos = session,Infos =data)
        # Inicio de Tabla Recibo Fulfilment 
        elif  session['FcName'] == 'Fullfilment' and session['tabla'] =='recibo':
          if 'valor' in request.form:
            if len(request.form['valor'])>0:
              session['filtro']=request.form['filtro']
              session['valor']=request.form['valor']
              if len(request.form['inicio'])>0:
                session['inicio']=request.form['inicio']
                if len(request.form['fin'])>0:
                  session['fin']=request.form['fin']
                  cur = mysql.connection.cursor()
                  cur.execute('SELECT * FROM recibo_fc WHERE {} LIKE \'%{}%\' AND dia BETWEEN \'{}\' AND \'{}\' LIMIT {}, {}'.format(session['filtro'],session['valor'],session['inicio'],session['fin'],row1,row2))
                  data = cur.fetchall()
                  return render_template('reportes.html',Datos = session,Infos =data)
                else:
                  cur = mysql.connection.cursor()
                  cur.execute('SELECT * FROM recibo_fc WHERE {} LIKE \'%{}%\' AND dia = \'{}\'  LIMIT {}, {}'.format(session['filtro'],session['valor'],session['inicio'],row1,row2))
                  data = cur.fetchall()
                  return render_template('reportes.html',Datos = session,Infos =data)
              else:
                cur = mysql.connection.cursor()
                cur.execute('SELECT * FROM recibo_fc WHERE {} LIKE \'%{}%\' LIMIT {}, {}'.format(session['filtro'],session['valor'],row1,row2))
                data = cur.fetchall()
                return render_template('reportes.html',Datos = session,Infos =data)
            else:
              cur = mysql.connection.cursor()
              cur.execute('SELECT * FROM recibo_fc LIMIT {}, {}'.format(row1,row2))
              data = cur.fetchall()
              return render_template('reportes.html',Datos = session,Infos =data) 
          else:
            cur = mysql.connection.cursor()
            cur.execute('SELECT * FROM recibo_fc LIMIT {}, {}'.format(row1,row2))
            data = cur.fetchall()
            return render_template('reportes.html',Datos = session,Infos =data)
        # Inicio de Tabla No Procesable Fulfilment 
        elif  session['FcName'] == 'Fullfilment' and session['tabla'] =='no_procesable':
          if 'valor' in request.form:
            if len(request.form['valor'])>0:
              session['filtro']=request.form['filtro']
              session['valor']=request.form['valor']
              if len(request.form['inicio'])>0:
                session['inicio']=request.form['inicio']
                if len(request.form['fin'])>0:
                  session['fin']=request.form['fin']
                  cur = mysql.connection.cursor()
                  cur.execute('SELECT * FROM ordenes_no_procesables WHERE {} LIKE \'%{}%\' AND fecha BETWEEN \'{}\' AND \'{}\' LIMIT {}, {}'.format(session['filtro'],session['valor'],session['inicio'],session['fin'],row1,row2))
                  data = cur.fetchall()
                  return render_template('reportes.html',Datos = session,Infos =data)
                else:
                  cur = mysql.connection.cursor()
                  cur.execute('SELECT * FROM ordenes_no_procesables WHERE {} LIKE \'%{}%\' AND fecha = \'{}\'  LIMIT {}, {}'.format(session['filtro'],session['valor'],session['inicio'],row1,row2))
                  data = cur.fetchall()
                  return render_template('reportes.html',Datos = session,Infos =data)
              else:
                cur = mysql.connection.cursor()
                cur.execute('SELECT * FROM ordenes_no_procesables WHERE {} LIKE \'%{}%\' LIMIT {}, {}'.format(session['filtro'],session['valor'],row1,row2))
                data = cur.fetchall()
                return render_template('reportes.html',Datos = session,Infos =data)
            else:
              cur = mysql.connection.cursor()
              cur.execute('SELECT * FROM ordenes_no_procesables LIMIT {}, {}'.format(row1,row2))
              data = cur.fetchall()
              return render_template('reportes.html',Datos = session,Infos =data) 
          else:
            cur = mysql.connection.cursor()
            cur.execute('SELECT * FROM ordenes_no_procesables LIMIT {}, {}'.format(row1,row2))
            data = cur.fetchall()
            return render_template('reportes.html',Datos = session,Infos =data)
        # Inicio de Tabla Prealert 
        elif  session['tabla'] =='prealert':
          if 'valor' in request.form:
            if len(request.form['valor'])>0:
              session['filtro']=request.form['filtro']
              session['valor']=request.form['valor']
              if len(request.form['inicio'])>0:
                session['inicio']=request.form['inicio']
                if len(request.form['fin'])>0:
                  session['fin']=request.form['fin']
                  cur = mysql.connection.cursor()
                  cur.execute('SELECT * FROM prealert WHERE {} LIKE \'%{}%\' AND dia BETWEEN \'{}\' AND \'{}\' LIMIT {}, {}'.format(session['filtro'],session['valor'],session['inicio'],session['fin'],row1,row2))
                  data = cur.fetchall()
                  return render_template('reportes.html',Datos = session,Infos =data)
                else:
                  cur = mysql.connection.cursor()
                  cur.execute('SELECT * FROM prealert WHERE {} LIKE \'%{}%\' AND dia = \'{}\'  LIMIT {}, {}'.format(session['filtro'],session['valor'],session['inicio'],row1,row2))
                  data = cur.fetchall()
                  return render_template('reportes.html',Datos = session,Infos =data)
              else:
                cur = mysql.connection.cursor()
                cur.execute('SELECT * FROM prealert WHERE {} LIKE \'%{}%\' LIMIT {}, {}'.format(session['filtro'],session['valor'],row1,row2))
                data = cur.fetchall()
                return render_template('reportes.html',Datos = session,Infos =data)
            else:
              cur = mysql.connection.cursor()
              cur.execute('SELECT * FROM prealert LIMIT {}, {}'.format(row1,row2))
              data = cur.fetchall()
              return render_template('reportes.html',Datos = session,Infos =data) 
          else:
            cur = mysql.connection.cursor()
            cur.execute('SELECT * FROM prealert LIMIT {}, {}'.format(row1,row2))
            data = cur.fetchall()
            return render_template('reportes.html',Datos = session,Infos =data)
        # Inicio de Tabla Entradas  Service Center 
        elif  session['FcName'] == 'Service Center' and session['tabla'] =='Entrada':
          if 'valor' in request.form:
            if len(request.form['valor'])>0:
              session['filtro']=request.form['filtro']
              session['valor']=request.form['valor']
              if len(request.form['inicio'])>0:
                session['inicio']=request.form['inicio']
                if len(request.form['fin'])>0:
                  session['fin']=request.form['fin']
                  cur = mysql.connection.cursor()
                  cur.execute('SELECT * FROM entrada_svcs WHERE {} LIKE \'%{}%\' AND Fecha_Creación	 BETWEEN \'{}\' AND \'{}\' LIMIT {}, {}'.format(session['filtro'],session['valor'],session['inicio'],session['fin'],row1,row2))
                  data = cur.fetchall()
                  return render_template('reportes.html',Datos = session,Infos =data)
                else:
                  cur = mysql.connection.cursor()
                  cur.execute('SELECT * FROM entrada_svcs WHERE {} LIKE \'%{}%\' AND Fecha_Creación	 = \'{}\'  LIMIT {}, {}'.format(session['filtro'],session['valor'],session['inicio'],row1,row2))
                  data = cur.fetchall()
                  return render_template('reportes.html',Datos = session,Infos =data)
              else:
                cur = mysql.connection.cursor()
                cur.execute('SELECT * FROM entrada_svcs WHERE {} LIKE \'%{}%\' LIMIT {}, {}'.format(session['filtro'],session['valor'],row1,row2))
                data = cur.fetchall()
                return render_template('reportes.html',Datos = session,Infos =data)
            else:
              cur = mysql.connection.cursor()
              cur.execute('SELECT * FROM entrada_svcs LIMIT {}, {}'.format(row1,row2))
              data = cur.fetchall()
              return render_template('reportes.html',Datos = session,Infos =data) 
          else:
            cur = mysql.connection.cursor()
            cur.execute('SELECT * FROM entrada_svcs LIMIT {}, {}'.format(row1,row2))
            data = cur.fetchall()
            return render_template('reportes.html',Datos = session,Infos =data)
        # Inicio de Tabla SalidaS Service Senter 
        elif  session['FcName'] == 'Service Center' and session['tabla'] =='Salida':
          if 'valor' in request.form:
            if len(request.form['valor'])>0:
              session['filtro']=request.form['filtro']
              session['valor']=request.form['valor']
              if len(request.form['inicio'])>0:
                session['inicio']=request.form['inicio']
                if len(request.form['fin'])>0:
                  session['fin']=request.form['fin']
                  cur = mysql.connection.cursor()
                  cur.execute('SELECT * FROM salida_svcs WHERE {} LIKE \'%{}%\' AND Fecha_Creación	 BETWEEN \'{}\' AND \'{}\' LIMIT {}, {}'.format(session['filtro'],session['valor'],session['inicio'],session['fin'],row1,row2))
                  data = cur.fetchall()
                  return render_template('reportes.html',Datos = session,Infos =data)
                else:
                  cur = mysql.connection.cursor()
                  cur.execute('SELECT * FROM salida_svcs WHERE {} LIKE \'%{}%\' AND Fecha_Creación	 = \'{}\'  LIMIT {}, {}'.format(session['filtro'],session['valor'],session['inicio'],row1,row2))
                  data = cur.fetchall()
                  return render_template('reportes.html',Datos = session,Infos =data)
              else:
                cur = mysql.connection.cursor()
                cur.execute('SELECT * FROM salida_svcs WHERE {} LIKE \'%{}%\' LIMIT {}, {}'.format(session['filtro'],session['valor'],row1,row2))
                data = cur.fetchall()
                return render_template('reportes.html',Datos = session,Infos =data)
            else:
              cur = mysql.connection.cursor()
              cur.execute('SELECT * FROM salida_svcs LIMIT {}, {}'.format(row1,row2))
              data = cur.fetchall()
              return render_template('reportes.html',Datos = session,Infos =data) 
          else:
            cur = mysql.connection.cursor()
            cur.execute('SELECT * FROM salida_svcs LIMIT {}, {}'.format(row1,row2))
            data = cur.fetchall()
            return render_template('reportes.html',Datos = session,Infos =data)
        # Inicio de Tabla Entradas  Cross Dock 
        elif  session['FcName'] == 'Cross Dock' and session['tabla'] =='Entrada':
          if 'valor' in request.form:
            if len(request.form['valor'])>0:
              session['filtro']=request.form['filtro']
              session['valor']=request.form['valor']
              if len(request.form['inicio'])>0:
                session['inicio']=request.form['inicio']
                if len(request.form['fin'])>0:
                  session['fin']=request.form['fin']
                  cur = mysql.connection.cursor()
                  cur.execute('SELECT * FROM entrada_xd WHERE {} LIKE \'%{}%\' AND Fecha_Creación	 BETWEEN \'{}\' AND \'{}\' LIMIT {}, {}'.format(session['filtro'],session['valor'],session['inicio'],session['fin'],row1,row2))
                  data = cur.fetchall()
                  return render_template('reportes.html',Datos = session,Infos =data)
                else:
                  cur = mysql.connection.cursor()
                  cur.execute('SELECT * FROM entrada_xd WHERE {} LIKE \'%{}%\' AND Fecha_Creación	 = \'{}\'  LIMIT {}, {}'.format(session['filtro'],session['valor'],session['inicio'],row1,row2))
                  data = cur.fetchall()
                  return render_template('reportes.html',Datos = session,Infos =data)
              else:
                cur = mysql.connection.cursor()
                cur.execute('SELECT * FROM entrada_xd WHERE {} LIKE \'%{}%\' LIMIT {}, {}'.format(session['filtro'],session['valor'],row1,row2))
                data = cur.fetchall()
                return render_template('reportes.html',Datos = session,Infos =data)
            else:
              cur = mysql.connection.cursor()
              cur.execute('SELECT * FROM entrada_xd LIMIT {}, {}'.format(row1,row2))
              data = cur.fetchall()
              return render_template('reportes.html',Datos = session,Infos =data) 
          else:
            cur = mysql.connection.cursor()
            cur.execute('SELECT * FROM entrada_xd LIMIT {}, {}'.format(row1,row2))
            data = cur.fetchall()
            return render_template('reportes.html',Datos = session,Infos =data)
        # Inicio de Tabla SalidaS Cross Dock 
        elif  session['FcName'] == 'Cross Dock' and session['tabla'] =='Salida':
          if 'valor' in request.form:
            if len(request.form['valor'])>0:
              session['filtro']=request.form['filtro']
              session['valor']=request.form['valor']
              if len(request.form['inicio'])>0:
                session['inicio']=request.form['inicio']
                if len(request.form['fin'])>0:
                  session['fin']=request.form['fin']
                  cur = mysql.connection.cursor()
                  cur.execute('SELECT * FROM salida_xd WHERE {} LIKE \'%{}%\' AND Fecha_Creación	 BETWEEN \'{}\' AND \'{}\' LIMIT {}, {}'.format(session['filtro'],session['valor'],session['inicio'],session['fin'],row1,row2))
                  data = cur.fetchall()
                  return render_template('reportes.html',Datos = session,Infos =data)
                else:
                  cur = mysql.connection.cursor()
                  cur.execute('SELECT * FROM salida_xd WHERE {} LIKE \'%{}%\' AND Fecha_Creación	 = \'{}\'  LIMIT {}, {}'.format(session['filtro'],session['valor'],session['inicio'],row1,row2))
                  data = cur.fetchall()
                  return render_template('reportes.html',Datos = session,Infos =data)
              else:
                cur = mysql.connection.cursor()
                cur.execute('SELECT * FROM salida_xd WHERE {} LIKE \'%{}%\' LIMIT {}, {}'.format(session['filtro'],session['valor'],row1,row2))
                data = cur.fetchall()
                return render_template('reportes.html',Datos = session,Infos =data)
            else:
              cur = mysql.connection.cursor()
              cur.execute('SELECT * FROM salida_xd LIMIT {}, {}'.format(row1,row2))
              data = cur.fetchall()
              return render_template('reportes.html',Datos = session,Infos =data) 
          else:
            cur = mysql.connection.cursor()
            cur.execute('SELECT * FROM salida_xd LIMIT {}, {}'.format(row1,row2))
            data = cur.fetchall()
            return render_template('reportes.html',Datos = session,Infos =data)
        # Inicio de Tabla Planning
        elif  session['tabla'] =='planning':
          if 'valor' in request.form:
            if len(request.form['valor'])>0:
              session['filtro']=request.form['filtro']
              session['valor']=request.form['valor']
              if len(request.form['inicio'])>0:
                session['inicio']=request.form['inicio']
                if len(request.form['fin'])>0:
                  session['fin']=request.form['fin']
                  cur = mysql.connection.cursor()
                  cur.execute('SELECT * FROM planing WHERE {} LIKE \'%{}%\' AND Fecha_Creación	 BETWEEN \'{}\' AND \'{}\' LIMIT {}, {}'.format(session['filtro'],session['valor'],session['inicio'],session['fin'],row1,row2))
                  data = cur.fetchall()
                  return render_template('reportes.html',Datos = session,Infos =data)
                else:
                  cur = mysql.connection.cursor()
                  cur.execute('SELECT * FROM planing WHERE {} LIKE \'%{}%\' AND Fecha_Creación	 = \'{}\'  LIMIT {}, {}'.format(session['filtro'],session['valor'],session['inicio'],row1,row2))
                  data = cur.fetchall()
                  return render_template('reportes.html',Datos = session,Infos =data)
              else:
                cur = mysql.connection.cursor()
                cur.execute('SELECT * FROM planing WHERE {} LIKE \'%{}%\' LIMIT {}, {}'.format(session['filtro'],session['valor'],row1,row2))
                data = cur.fetchall()
                return render_template('reportes.html',Datos = session,Infos =data)
            else:
              cur = mysql.connection.cursor()
              cur.execute('SELECT * FROM planing LIMIT {}, {}'.format(row1,row2))
              data = cur.fetchall()
              return render_template('reportes.html',Datos = session,Infos =data) 
          else:
            cur = mysql.connection.cursor()
            cur.execute('SELECT * FROM planing LIMIT {}, {}'.format(row1,row2))
            data = cur.fetchall()
            return render_template('reportes.html',Datos = session,Infos =data)
        else:
            return render_template('reportes.html',Datos = session)
      else: 
        if 'tabla' in session:
          if request.method == 'GET':
            session['rowi']=rowi
            row1 = int(session['rowi'])
            row2 = 50
          else:
            row1 = int(session['rowi'])
            row2 =50
          # Inicio de Tabla Entradas Fulfilment      
          if  session['FcName'] == 'Fullfilment' and session['tabla'] =='Entrada':
            if 'valor' in session:
              if len(session['valor'])>0:
                if 'inicio' in session:
                  if len(session['inicio'])>0:
                    if 'fin' in session:
                      if len(session['fin'])>0:
                        cur = mysql.connection.cursor()
                        cur.execute('SELECT * FROM entrada_fc WHERE {} LIKE \'%{}%\' AND Fecha_Creación BETWEEN \'{}\' AND \'{}\' LIMIT {}, {}'.format(session['filtro'],session['valor'],session['inicio'],session['fin'],row1,row2))
                        data = cur.fetchall()
                        return render_template('reportes.html',Datos = session,Infos =data)
                      else:
                        cur = mysql.connection.cursor()
                        cur.execute('SELECT * FROM entrada_fc WHERE {} LIKE \'%{}%\' AND Fecha_Creación = \'{}\'  LIMIT {}, {}'.format(session['filtro'],session['valor'],session['inicio'],row1,row2))
                        data = cur.fetchall()
                        return render_template('reportes.html',Datos = session,Infos =data)
                    else:
                        cur = mysql.connection.cursor()
                        cur.execute('SELECT * FROM entrada_fc WHERE {} LIKE \'%{}%\' AND Fecha_Creación = \'{}\'  LIMIT {}, {}'.format(session['filtro'],session['valor'],session['inicio'],row1,row2))
                        data = cur.fetchall()
                        return render_template('reportes.html',Datos = session,Infos =data)
                  else:
                    cur = mysql.connection.cursor()
                    cur.execute('SELECT * FROM entrada_fc WHERE {} LIKE \'%{}%\' LIMIT {}, {}'.format(session['filtro'],session['valor'],row1,row2))
                    data = cur.fetchall()
                    return render_template('reportes.html',Datos = session,Infos =data)  
                else:
                  cur = mysql.connection.cursor()
                  cur.execute('SELECT * FROM entrada_fc WHERE {} LIKE \'%{}%\' LIMIT {}, {}'.format(session['filtro'],session['valor'],row1,row2))
                  data = cur.fetchall()
                  return render_template('reportes.html',Datos = session,Infos =data)
              else:
                cur = mysql.connection.cursor()
                cur.execute('SELECT * FROM entrada_fc LIMIT {}, {}'.format(row1,row2))
                data = cur.fetchall()
                return render_template('reportes.html',Datos = session,Infos =data)
            else:
              cur = mysql.connection.cursor()
              cur.execute('SELECT * FROM entrada_fc LIMIT {}, {}'.format(row1,row2))
              data = cur.fetchall()
              return render_template('reportes.html',Datos = session,Infos =data)
          # Inicio de Tabla SalidaS Fulfilment        
          elif  session['FcName'] == 'Fullfilment' and session['tabla'] =='Salida':
            if 'valor' in session:
              if len(session['valor'])>0:
                if 'inicio' in session:
                  if len(session['inicio'])>0:
                    if 'fin' in session:
                      if len(session['fin'])>0:
                        cur = mysql.connection.cursor()
                        cur.execute('SELECT * FROM salida_fc WHERE {} LIKE \'%{}%\' AND Fecha_Creación BETWEEN \'{}\' AND \'{}\' LIMIT {}, {}'.format(session['filtro'],session['valor'],session['inicio'],session['fin'],row1,row2))
                        data = cur.fetchall()
                        return render_template('reportes.html',Datos = session,Infos =data)
                      else:
                        cur = mysql.connection.cursor()
                        cur.execute('SELECT * FROM salida_fc WHERE {} LIKE \'%{}%\' AND Fecha_Creación = \'{}\'  LIMIT {}, {}'.format(session['filtro'],session['valor'],session['inicio'],row1,row2))
                        data = cur.fetchall()
                        return render_template('reportes.html',Datos = session,Infos =data)
                    else:
                        cur = mysql.connection.cursor()
                        cur.execute('SELECT * FROM salida_fc WHERE {} LIKE \'%{}%\' AND Fecha_Creación = \'{}\'  LIMIT {}, {}'.format(session['filtro'],session['valor'],session['inicio'],row1,row2))
                        data = cur.fetchall()
                        return render_template('reportes.html',Datos = session,Infos =data)
                  else:
                    cur = mysql.connection.cursor()
                    cur.execute('SELECT * FROM salida_fc WHERE {} LIKE \'%{}%\' LIMIT {}, {}'.format(session['filtro'],session['valor'],row1,row2))
                    data = cur.fetchall()
                    return render_template('reportes.html',Datos = session,Infos =data)  
                else:
                  cur = mysql.connection.cursor()
                  cur.execute('SELECT * FROM salida_fc WHERE {} LIKE \'%{}%\' LIMIT {}, {}'.format(session['filtro'],session['valor'],row1,row2))
                  data = cur.fetchall()
                  return render_template('reportes.html',Datos = session,Infos =data)
              else:
                cur = mysql.connection.cursor()
                cur.execute('SELECT * FROM salida_fc LIMIT {}, {}'.format(row1,row2))
                data = cur.fetchall()
                return render_template('reportes.html',Datos = session,Infos =data)
            else:
              cur = mysql.connection.cursor()
              cur.execute('SELECT * FROM salida_fc LIMIT {}, {}'.format(row1,row2))
              data = cur.fetchall()
              return render_template('reportes.html',Datos = session,Infos =data)
          # Inicio de Tabla Transfer Fulfilment 
          elif  session['FcName'] == 'Fullfilment' and session['tabla'] =='Entrada_Tranferencias':
            if 'valor' in session:
              if len(session['valor'])>0:
                if 'inicio' in session:
                  if len(session['inicio'])>0:
                    if 'fin' in session:
                      if len(session['fin'])>0:
                        cur = mysql.connection.cursor()
                        cur.execute('SELECT * FROM entrada_tranferencias_fc WHERE {} LIKE \'%{}%\' AND Fecha_Creación BETWEEN \'{}\' AND \'{}\' LIMIT {}, {}'.format(session['filtro'],session['valor'],session['inicio'],session['fin'],row1,row2))
                        data = cur.fetchall()
                        return render_template('reportes.html',Datos = session,Infos =data)
                      else:
                        cur = mysql.connection.cursor()
                        cur.execute('SELECT * FROM entrada_tranferencias_fc WHERE {} LIKE \'%{}%\' AND Fecha_Creación = \'{}\'  LIMIT {}, {}'.format(session['filtro'],session['valor'],session['inicio'],row1,row2))
                        data = cur.fetchall()
                        return render_template('reportes.html',Datos = session,Infos =data)
                    else:
                        cur = mysql.connection.cursor()
                        cur.execute('SELECT * FROM entrada_tranferencias_fc WHERE {} LIKE \'%{}%\' AND Fecha_Creación = \'{}\'  LIMIT {}, {}'.format(session['filtro'],session['valor'],session['inicio'],row1,row2))
                        data = cur.fetchall()
                        return render_template('reportes.html',Datos = session,Infos =data)
                  else:
                    cur = mysql.connection.cursor()
                    cur.execute('SELECT * FROM entrada_tranferencias_fc WHERE {} LIKE \'%{}%\' LIMIT {}, {}'.format(session['filtro'],session['valor'],row1,row2))
                    data = cur.fetchall()
                    return render_template('reportes.html',Datos = session,Infos =data)  
                else:
                  cur = mysql.connection.cursor()
                  cur.execute('SELECT * FROM entrada_tranferencias_fc WHERE {} LIKE \'%{}%\' LIMIT {}, {}'.format(session['filtro'],session['valor'],row1,row2))
                  data = cur.fetchall()
                  return render_template('reportes.html',Datos = session,Infos =data)
              else:
                cur = mysql.connection.cursor()
                cur.execute('SELECT * FROM entrada_tranferencias_fc LIMIT {}, {}'.format(row1,row2))
                data = cur.fetchall()
                return render_template('reportes.html',Datos = session,Infos =data)
            else:
              cur = mysql.connection.cursor()
              cur.execute('SELECT * FROM entrada_tranferencias_fc LIMIT {}, {}'.format(row1,row2))
              data = cur.fetchall()
              return render_template('reportes.html',Datos = session,Infos =data)
          # Inicio de Tabla Recibo Fulfilment 
          elif  session['FcName'] == 'Fullfilment' and session['tabla'] =='recibo':
            if 'valor' in session:
              if len(session['valor'])>0:
                if 'inicio' in session:
                  if len(session['inicio'])>0:
                    if 'fin' in session:
                      if len(session['fin'])>0:
                        cur = mysql.connection.cursor()
                        cur.execute('SELECT * FROM recibo_fc WHERE {} LIKE \'%{}%\' AND dia BETWEEN \'{}\' AND \'{}\' LIMIT {}, {}'.format(session['filtro'],session['valor'],session['inicio'],session['fin'],row1,row2))
                        data = cur.fetchall()
                        return render_template('reportes.html',Datos = session,Infos =data)
                      else:
                        cur = mysql.connection.cursor()
                        cur.execute('SELECT * FROM recibo_fc WHERE {} LIKE \'%{}%\' AND dia = \'{}\'  LIMIT {}, {}'.format(session['filtro'],session['valor'],session['inicio'],row1,row2))
                        data = cur.fetchall()
                        return render_template('reportes.html',Datos = session,Infos =data)
                    else:
                        cur = mysql.connection.cursor()
                        cur.execute('SELECT * FROM recibo_fc WHERE {} LIKE \'%{}%\' AND dia = \'{}\'  LIMIT {}, {}'.format(session['filtro'],session['valor'],session['inicio'],row1,row2))
                        data = cur.fetchall()
                        return render_template('reportes.html',Datos = session,Infos =data)
                  else:
                    cur = mysql.connection.cursor()
                    cur.execute('SELECT * FROM recibo_fc WHERE {} LIKE \'%{}%\' LIMIT {}, {}'.format(session['filtro'],session['valor'],row1,row2))
                    data = cur.fetchall()
                    return render_template('reportes.html',Datos = session,Infos =data)  
                else:
                  cur = mysql.connection.cursor()
                  cur.execute('SELECT * FROM recibo_fc WHERE {} LIKE \'%{}%\' LIMIT {}, {}'.format(session['filtro'],session['valor'],row1,row2))
                  data = cur.fetchall()
                  return render_template('reportes.html',Datos = session,Infos =data)
              else:
                cur = mysql.connection.cursor()
                cur.execute('SELECT * FROM recibo_fc LIMIT {}, {}'.format(row1,row2))
                data = cur.fetchall()
                return render_template('reportes.html',Datos = session,Infos =data)
            else:
              cur = mysql.connection.cursor()
              cur.execute('SELECT * FROM recibo_fc LIMIT {}, {}'.format(row1,row2))
              data = cur.fetchall()
              return render_template('reportes.html',Datos = session,Infos =data)
          # Inicio de Tabla No Procesable Fulfilment 
          elif  session['FcName'] == 'Fullfilment' and session['tabla'] =='no_procesable':
            if 'valor' in session:
              if len(session['valor'])>0:
                if 'inicio' in session:
                  if len(session['inicio'])>0:
                    if 'fin' in session:
                      if len(session['fin'])>0:
                        cur = mysql.connection.cursor()
                        cur.execute('SELECT * FROM ordenes_no_procesables WHERE {} LIKE \'%{}%\' AND dia BETWEEN \'{}\' AND \'{}\' LIMIT {}, {}'.format(session['filtro'],session['valor'],session['inicio'],session['fin'],row1,row2))
                        data = cur.fetchall()
                        return render_template('reportes.html',Datos = session,Infos =data)
                      else:
                        cur = mysql.connection.cursor()
                        cur.execute('SELECT * FROM ordenes_no_procesables WHERE {} LIKE \'%{}%\' AND dia = \'{}\'  LIMIT {}, {}'.format(session['filtro'],session['valor'],session['inicio'],row1,row2))
                        data = cur.fetchall()
                        return render_template('reportes.html',Datos = session,Infos =data)
                    else:
                        cur = mysql.connection.cursor()
                        cur.execute('SELECT * FROM ordenes_no_procesables WHERE {} LIKE \'%{}%\' AND dia = \'{}\'  LIMIT {}, {}'.format(session['filtro'],session['valor'],session['inicio'],row1,row2))
                        data = cur.fetchall()
                        return render_template('reportes.html',Datos = session,Infos =data)
                  else:
                    cur = mysql.connection.cursor()
                    cur.execute('SELECT * FROM ordenes_no_procesables WHERE {} LIKE \'%{}%\' LIMIT {}, {}'.format(session['filtro'],session['valor'],row1,row2))
                    data = cur.fetchall()
                    return render_template('reportes.html',Datos = session,Infos =data)  
                else:
                  cur = mysql.connection.cursor()
                  cur.execute('SELECT * FROM ordenes_no_procesables WHERE {} LIKE \'%{}%\' LIMIT {}, {}'.format(session['filtro'],session['valor'],row1,row2))
                  data = cur.fetchall()
                  return render_template('reportes.html',Datos = session,Infos =data)
              else:
                cur = mysql.connection.cursor()
                cur.execute('SELECT * FROM ordenes_no_procesables LIMIT {}, {}'.format(row1,row2))
                data = cur.fetchall()
                return render_template('reportes.html',Datos = session,Infos =data)
            else:
              cur = mysql.connection.cursor()
              cur.execute('SELECT * FROM ordenes_no_procesables LIMIT {}, {}'.format(row1,row2))
              data = cur.fetchall()
              return render_template('reportes.html',Datos = session,Infos =data)
          # Inicio de Tabla Prealert 
          elif  session['tabla'] =='prealert':
            if 'valor' in session:
              if len(session['valor'])>0:
                if 'inicio' in session:
                  if len(session['inicio'])>0:
                    if 'fin' in session:
                      if len(session['fin'])>0:
                        cur = mysql.connection.cursor()
                        cur.execute('SELECT * FROM prealert WHERE {} LIKE \'%{}%\' AND dia BETWEEN \'{}\' AND \'{}\' LIMIT {}, {}'.format(session['filtro'],session['valor'],session['inicio'],session['fin'],row1,row2))
                        data = cur.fetchall()
                        return render_template('reportes.html',Datos = session,Infos =data)
                      else:
                        cur = mysql.connection.cursor()
                        cur.execute('SELECT * FROM prealert WHERE {} LIKE \'%{}%\' AND dia = \'{}\'  LIMIT {}, {}'.format(session['filtro'],session['valor'],session['inicio'],row1,row2))
                        data = cur.fetchall()
                        return render_template('reportes.html',Datos = session,Infos =data)
                    else:
                        cur = mysql.connection.cursor()
                        cur.execute('SELECT * FROM prealert WHERE {} LIKE \'%{}%\' AND dia = \'{}\'  LIMIT {}, {}'.format(session['filtro'],session['valor'],session['inicio'],row1,row2))
                        data = cur.fetchall()
                        return render_template('reportes.html',Datos = session,Infos =data)
                  else:
                    cur = mysql.connection.cursor()
                    cur.execute('SELECT * FROM prealert WHERE {} LIKE \'%{}%\' LIMIT {}, {}'.format(session['filtro'],session['valor'],row1,row2))
                    data = cur.fetchall()
                    return render_template('reportes.html',Datos = session,Infos =data)  
                else:
                  cur = mysql.connection.cursor()
                  cur.execute('SELECT * FROM prealert WHERE {} LIKE \'%{}%\' LIMIT {}, {}'.format(session['filtro'],session['valor'],row1,row2))
                  data = cur.fetchall()
                  return render_template('reportes.html',Datos = session,Infos =data)
              else:
                cur = mysql.connection.cursor()
                cur.execute('SELECT * FROM prealert LIMIT {}, {}'.format(row1,row2))
                data = cur.fetchall()
                return render_template('reportes.html',Datos = session,Infos =data)
            else:
              cur = mysql.connection.cursor()
              cur.execute('SELECT * FROM prealert LIMIT {}, {}'.format(row1,row2))
              data = cur.fetchall()
              return render_template('reportes.html',Datos = session,Infos =data)
          # Inicio de Tabla Entradas  Service Center 
          elif  session['FcName'] == 'Service Center' and session['tabla'] =='Entrada':
            if 'valor' in session:
              if len(session['valor'])>0:
                if 'inicio' in session:
                  if len(session['inicio'])>0:
                    if 'fin' in session:
                      if len(session['fin'])>0:
                        cur = mysql.connection.cursor()
                        cur.execute('SELECT * FROM entrada_svcs WHERE {} LIKE \'%{}%\' AND Fecha_Creación BETWEEN \'{}\' AND \'{}\' LIMIT {}, {}'.format(session['filtro'],session['valor'],session['inicio'],session['fin'],row1,row2))
                        data = cur.fetchall()
                        return render_template('reportes.html',Datos = session,Infos =data)
                      else:
                        cur = mysql.connection.cursor()
                        cur.execute('SELECT * FROM entrada_svcs WHERE {} LIKE \'%{}%\' AND Fecha_Creación = \'{}\'  LIMIT {}, {}'.format(session['filtro'],session['valor'],session['inicio'],row1,row2))
                        data = cur.fetchall()
                        return render_template('reportes.html',Datos = session,Infos =data)
                    else:
                        cur = mysql.connection.cursor()
                        cur.execute('SELECT * FROM entrada_svcs WHERE {} LIKE \'%{}%\' AND Fecha_Creación = \'{}\'  LIMIT {}, {}'.format(session['filtro'],session['valor'],session['inicio'],row1,row2))
                        data = cur.fetchall()
                        return render_template('reportes.html',Datos = session,Infos =data)
                  else:
                    cur = mysql.connection.cursor()
                    cur.execute('SELECT * FROM entrada_svcs WHERE {} LIKE \'%{}%\' LIMIT {}, {}'.format(session['filtro'],session['valor'],row1,row2))
                    data = cur.fetchall()
                    return render_template('reportes.html',Datos = session,Infos =data)  
                else:
                  cur = mysql.connection.cursor()
                  cur.execute('SELECT * FROM entrada_svcs WHERE {} LIKE \'%{}%\' LIMIT {}, {}'.format(session['filtro'],session['valor'],row1,row2))
                  data = cur.fetchall()
                  return render_template('reportes.html',Datos = session,Infos =data)
              else:
                cur = mysql.connection.cursor()
                cur.execute('SELECT * FROM entrada_svcs LIMIT {}, {}'.format(row1,row2))
                data = cur.fetchall()
                return render_template('reportes.html',Datos = session,Infos =data)
            else:
              cur = mysql.connection.cursor()
              cur.execute('SELECT * FROM entrada_svcs LIMIT {}, {}'.format(row1,row2))
              data = cur.fetchall()
              return render_template('reportes.html',Datos = session,Infos =data)
          # Inicio de Tabla SalidaS Service Senter 
          elif  session['FcName'] == 'Service Center' and session['tabla'] =='Salida':
            if 'valor' in session:
              if len(session['valor'])>0:
                if 'inicio' in session:
                  if len(session['inicio'])>0:
                    if 'fin' in session:
                      if len(session['fin'])>0:
                        cur = mysql.connection.cursor()
                        cur.execute('SELECT * FROM salida_svcs WHERE {} LIKE \'%{}%\' AND Fecha_Creación BETWEEN \'{}\' AND \'{}\' LIMIT {}, {}'.format(session['filtro'],session['valor'],session['inicio'],session['fin'],row1,row2))
                        data = cur.fetchall()
                        return render_template('reportes.html',Datos = session,Infos =data)
                      else:
                        cur = mysql.connection.cursor()
                        cur.execute('SELECT * FROM salida_svcs WHERE {} LIKE \'%{}%\' AND Fecha_Creación = \'{}\'  LIMIT {}, {}'.format(session['filtro'],session['valor'],session['inicio'],row1,row2))
                        data = cur.fetchall()
                        return render_template('reportes.html',Datos = session,Infos =data)
                    else:
                        cur = mysql.connection.cursor()
                        cur.execute('SELECT * FROM salida_svcs WHERE {} LIKE \'%{}%\' AND Fecha_Creación = \'{}\'  LIMIT {}, {}'.format(session['filtro'],session['valor'],session['inicio'],row1,row2))
                        data = cur.fetchall()
                        return render_template('reportes.html',Datos = session,Infos =data)
                  else:
                    cur = mysql.connection.cursor()
                    cur.execute('SELECT * FROM salida_svcs WHERE {} LIKE \'%{}%\' LIMIT {}, {}'.format(session['filtro'],session['valor'],row1,row2))
                    data = cur.fetchall()
                    return render_template('reportes.html',Datos = session,Infos =data)  
                else:
                  cur = mysql.connection.cursor()
                  cur.execute('SELECT * FROM salida_svcs WHERE {} LIKE \'%{}%\' LIMIT {}, {}'.format(session['filtro'],session['valor'],row1,row2))
                  data = cur.fetchall()
                  return render_template('reportes.html',Datos = session,Infos =data)
              else:
                cur = mysql.connection.cursor()
                cur.execute('SELECT * FROM salida_svcs LIMIT {}, {}'.format(row1,row2))
                data = cur.fetchall()
                return render_template('reportes.html',Datos = session,Infos =data)
            else:
              cur = mysql.connection.cursor()
              cur.execute('SELECT * FROM salida_svcs LIMIT {}, {}'.format(row1,row2))
              data = cur.fetchall()
              return render_template('reportes.html',Datos = session,Infos =data)
          # Inicio de Tabla Entradas  Cross Dock 
          elif  session['FcName'] == 'Cross Dock' and session['tabla'] =='Entrada':
            if 'valor' in session:
              if len(session['valor'])>0:
                if 'inicio' in session:
                  if len(session['inicio'])>0:
                    if 'fin' in session:
                      if len(session['fin'])>0:
                        cur = mysql.connection.cursor()
                        cur.execute('SELECT * FROM entrada_xd WHERE {} LIKE \'%{}%\' AND Fecha_Creación BETWEEN \'{}\' AND \'{}\' LIMIT {}, {}'.format(session['filtro'],session['valor'],session['inicio'],session['fin'],row1,row2))
                        data = cur.fetchall()
                        return render_template('reportes.html',Datos = session,Infos =data)
                      else:
                        cur = mysql.connection.cursor()
                        cur.execute('SELECT * FROM entrada_xd WHERE {} LIKE \'%{}%\' AND Fecha_Creación = \'{}\'  LIMIT {}, {}'.format(session['filtro'],session['valor'],session['inicio'],row1,row2))
                        data = cur.fetchall()
                        return render_template('reportes.html',Datos = session,Infos =data)
                    else:
                        cur = mysql.connection.cursor()
                        cur.execute('SELECT * FROM entrada_xd WHERE {} LIKE \'%{}%\' AND Fecha_Creación = \'{}\'  LIMIT {}, {}'.format(session['filtro'],session['valor'],session['inicio'],row1,row2))
                        data = cur.fetchall()
                        return render_template('reportes.html',Datos = session,Infos =data)
                  else:
                    cur = mysql.connection.cursor()
                    cur.execute('SELECT * FROM entrada_xd WHERE {} LIKE \'%{}%\' LIMIT {}, {}'.format(session['filtro'],session['valor'],row1,row2))
                    data = cur.fetchall()
                    return render_template('reportes.html',Datos = session,Infos =data)  
                else:
                  cur = mysql.connection.cursor()
                  cur.execute('SELECT * FROM entrada_xd WHERE {} LIKE \'%{}%\' LIMIT {}, {}'.format(session['filtro'],session['valor'],row1,row2))
                  data = cur.fetchall()
                  return render_template('reportes.html',Datos = session,Infos =data)
              else:
                cur = mysql.connection.cursor()
                cur.execute('SELECT * FROM entrada_xd LIMIT {}, {}'.format(row1,row2))
                data = cur.fetchall()
                return render_template('reportes.html',Datos = session,Infos =data)
            else:
              cur = mysql.connection.cursor()
              cur.execute('SELECT * FROM entrada_xd LIMIT {}, {}'.format(row1,row2))
              data = cur.fetchall()
              return render_template('reportes.html',Datos = session,Infos =data)
          # Inicio de Tabla SalidaS Cross Dock 
          elif  session['FcName'] == 'Cross Dock' and session['tabla'] =='Salida':
            if 'valor' in session:
              if len(session['valor'])>0:
                if 'inicio' in session:
                  if len(session['inicio'])>0:
                    if 'fin' in session:
                      if len(session['fin'])>0:
                        cur = mysql.connection.cursor()
                        cur.execute('SELECT * FROM salida_xd WHERE {} LIKE \'%{}%\' AND Fecha_Creación BETWEEN \'{}\' AND \'{}\' LIMIT {}, {}'.format(session['filtro'],session['valor'],session['inicio'],session['fin'],row1,row2))
                        data = cur.fetchall()
                        return render_template('reportes.html',Datos = session,Infos =data)
                      else:
                        cur = mysql.connection.cursor()
                        cur.execute('SELECT * FROM salida_xd WHERE {} LIKE \'%{}%\' AND Fecha_Creación = \'{}\'  LIMIT {}, {}'.format(session['filtro'],session['valor'],session['inicio'],row1,row2))
                        data = cur.fetchall()
                        return render_template('reportes.html',Datos = session,Infos =data)
                    else:
                        cur = mysql.connection.cursor()
                        cur.execute('SELECT * FROM salida_xd WHERE {} LIKE \'%{}%\' AND Fecha_Creación = \'{}\'  LIMIT {}, {}'.format(session['filtro'],session['valor'],session['inicio'],row1,row2))
                        data = cur.fetchall()
                        return render_template('reportes.html',Datos = session,Infos =data)
                  else:
                    cur = mysql.connection.cursor()
                    cur.execute('SELECT * FROM salida_xd WHERE {} LIKE \'%{}%\' LIMIT {}, {}'.format(session['filtro'],session['valor'],row1,row2))
                    data = cur.fetchall()
                    return render_template('reportes.html',Datos = session,Infos =data)  
                else:
                  cur = mysql.connection.cursor()
                  cur.execute('SELECT * FROM salida_xd WHERE {} LIKE \'%{}%\' LIMIT {}, {}'.format(session['filtro'],session['valor'],row1,row2))
                  data = cur.fetchall()
                  return render_template('reportes.html',Datos = session,Infos =data)
              else:
                cur = mysql.connection.cursor()
                cur.execute('SELECT * FROM salida_xd LIMIT {}, {}'.format(row1,row2))
                data = cur.fetchall()
                return render_template('reportes.html',Datos = session,Infos =data)
            else:
              cur = mysql.connection.cursor()
              cur.execute('SELECT * FROM salida_xd LIMIT {}, {}'.format(row1,row2))
              data = cur.fetchall()
              return render_template('reportes.html',Datos = session,Infos =data)
          # Inicio de Tabla Planning
          elif  session['tabla'] =='planning':
            if 'valor' in session:
              if len(session['valor'])>0:
                if 'inicio' in session:
                  if len(session['inicio'])>0:
                    if 'fin' in session:
                      if len(session['fin'])>0:
                        cur = mysql.connection.cursor()
                        cur.execute('SELECT * FROM planing WHERE {} LIKE \'%{}%\' AND Fecha_agendada BETWEEN \'{}\' AND \'{}\' LIMIT {}, {}'.format(session['filtro'],session['valor'],session['inicio'],session['fin'],row1,row2))
                        data = cur.fetchall()
                        return render_template('reportes.html',Datos = session,Infos =data)
                      else:
                        cur = mysql.connection.cursor()
                        cur.execute('SELECT * FROM planing WHERE {} LIKE \'%{}%\' AND Fecha_agendada = \'{}\'  LIMIT {}, {}'.format(session['filtro'],session['valor'],session['inicio'],row1,row2))
                        data = cur.fetchall()
                        return render_template('reportes.html',Datos = session,Infos =data)
                    else:
                        cur = mysql.connection.cursor()
                        cur.execute('SELECT * FROM planing WHERE {} LIKE \'%{}%\' AND Fecha_agendada = \'{}\'  LIMIT {}, {}'.format(session['filtro'],session['valor'],session['inicio'],row1,row2))
                        data = cur.fetchall()
                        return render_template('reportes.html',Datos = session,Infos =data)
                  else:
                    cur = mysql.connection.cursor()
                    cur.execute('SELECT * FROM planing WHERE {} LIKE \'%{}%\' LIMIT {}, {}'.format(session['filtro'],session['valor'],row1,row2))
                    data = cur.fetchall()
                    return render_template('reportes.html',Datos = session,Infos =data)  
                else:
                  cur = mysql.connection.cursor()
                  cur.execute('SELECT * FROM planing WHERE {} LIKE \'%{}%\' LIMIT {}, {}'.format(session['filtro'],session['valor'],row1,row2))
                  data = cur.fetchall()
                  return render_template('reportes.html',Datos = session,Infos =data)
              else:
                cur = mysql.connection.cursor()
                cur.execute('SELECT * FROM planing LIMIT {}, {}'.format(row1,row2))
                data = cur.fetchall()
                return render_template('reportes.html',Datos = session,Infos =data)
            else:
              cur = mysql.connection.cursor()
              cur.execute('SELECT * FROM planing LIMIT {}, {}'.format(row1,row2))
              data = cur.fetchall()
              return render_template('reportes.html',Datos = session,Infos =data)
          else:
            return render_template('reportes.html',Datos = session)
        else:
          session['tabla']= None
          session['rowi']= 0  
          return render_template('reportes.html',Datos = session)
  # except:
  #   flash("Inicia Secion")
  #   return render_template('index.html')


if __name__=='__main__':
    app.run(port = 3000, debug =True)