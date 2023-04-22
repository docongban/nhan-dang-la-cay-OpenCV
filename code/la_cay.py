import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="admin",
  database="la_cay"
)

def save(code, name):
    mycursor = mydb.cursor()
    sql = "INSERT INTO la (code, name) VALUES (%s, %s)"
    val = (code,name)
    mycursor.execute(sql, val)
    mydb.commit()

save('bac_ha', 'Lá bạc hà')
save('hung_chanh', 'Lá húng chanh')
save('hung_lui', 'Lá húng lũi')
save('hung_que', 'Lá húng quế')
save('kinh_gioi', 'Rau kinh giới')
save('la_lot', 'Lá lốt')
save('la_mo', 'Lá mơ')
save('rau_diep_ca', 'Rau diếp cá')
save('rau_ram', 'Rau răm')
save('tia_to', 'Tía tô')