import streamlit as st
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt 
import seaborn as sns

#DB Management
import sqlite3 
conn = sqlite3.connect('data.db')
c = conn.cursor()

def create_usertable():
	c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')

def distribution_plot(input_df, input_data):
	fig = plt.figure(figsize= (10,8))
	sns.scatterplot(data= input_df, x=input_data, y= "RR")
	st.pyplot(fig)

def input_number(input):
	number = st.number_input(input)
	return number

def curah_hujan(param_1 , param_2, param_3):
	y_Value = param_1 + (param_2 * param_3)
	return y_Value

def ramalan_cuaca (value_pred):
	if value_pred < 1:
		st.subheader("CERAH")
	elif value_pred >= 1 and value_pred < 5:
		st.subheader("Hujan Ringan")
	else:
		st.subheader("Hujan")

def df_calculate(input_param):
	if input_param == "SUHU":
		df = pd.read_csv(r"C:/Users/keceb/Documents/Python/Github-lathihan/data_suhu.csv")
		return df
	else:
		df = pd.read_csv(r"C:/Users/keceb/Documents/Python/Github-lathihan/data_kelembaban.csv")
		return df

def add_userdata(username,password):
	c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
	conn.commit()

def login_user(username,password):
	c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
	data = c.fetchall()
	return data

def view_all_users():
	c.execute('SELECT * FROM userstable')
	data = c.fetchall()
	return data



st.title("Prakiraan Cuaca Streamlit")

menu = ["Home","Login","SignUp"]
choice = st.sidebar.selectbox("Menu",menu)

if choice == "Home":
		st.subheader("Home")

elif choice == "Login":
		st.subheader("Login Section")

		username = st.sidebar.text_input("User Name")
		password = st.sidebar.text_input("Password",type='password')

		if	st.sidebar.checkbox("Login"):
				create_usertable()
				result = login_user(username,password)
				if result:
					st.success("Logged In as {}".format(username))
	
					task = st.selectbox("Task",["Add Post","Analytics","Profiles"])
					if task == "Add Post":
						st.subheader("Add Your Post")
						p_date = st.date_input("Tanggal Prediksi"
						, datetime(2023, 1, 1))
						option_cal = st.selectbox("Parameter", ("SUHU", "KELEMBABAN"))
						value_param = input_number(option_cal)
						df3 = df_calculate(option_cal)
						month = p_date.month
						df3 = df3.loc[df3["BULAN"] == month]
						a_Param = float(df3.iloc[0,1])
						b_Param = float(df3.iloc[0,2])
						pred_val = curah_hujan(a_Param, b_Param, value_param)
						st.write("Prediksi curah hujan: ", round(pred_val, 2))
						ramalan_cuaca(pred_val)

					elif task == "Analytics":
						st.subheader("Analytics")
						df = pd.read_csv(r"C:/Users/keceb/Documents/Python/Github-lathihan/data_cuaca.csv")
						df["Tahun"] = df["Tahun"].astype(str)
						st.dataframe(df)
						option = st.multiselect("Filter of Graphic",
						["RR","Prediction_base_on_RH","Prediction_base_on_T"],
						"RR")
						start_date = st.date_input(
    						"Filter Start date",
    						datetime(2020, 1, 1))
						end_date = st.date_input(
    						"Filter end date",
    						datetime(2021, 1, 1))
						df2 = df[["Tanggal","RR","Prediction_base_on_RH","Prediction_base_on_T","T_avg","RH_avg"]]
						df2.set_index("Tanggal", drop= True, inplace= True)
						df2 = df2.loc[str(start_date):str(end_date), ]
						st.line_chart(data= df2 , y = option)
						with st.expander("Suhu dan Kelembaban"):
							tab1, tab2 = st.tabs(["Suhu","Kelembaban"])
							with tab1:
								st.subheader("SUHU")
								st.line_chart(data= df2, y = "T_avg")
							with tab2:
								st.subheader("KELEMBABAN")
								st.line_chart(data= df2, y = "RH_avg")
						with st.expander("Distribusi Suhu, Kelembaban & Curah Hujan"):
							tab1, tab2 = st.tabs(["Suhu","Kelembaban"])
							with tab1:
								distribution_plot(df2, "T_avg")
							with tab2:
								distribution_plot(df2, "RH_avg")
					elif task == "Profiles":
						st.subheader("User Profiles")
						user_result = view_all_users()
						clean_db = pd.DataFrame(user_result,columns=["Username","Password"])
						st.dataframe(clean_db)
				else:
					st.warning("Incorrect Username/Password")
			


elif choice == "SignUp":
	st.subheader("Create New Account")		
	new_user = st.text_input("Username")
	new_password = st.text_input("Password",type='password')

	if st.button("Signup"):	
		create_usertable()
		add_userdata(new_user,new_password)		
		st.success("You have successfully created a valid Account")
		st.info("Go to Login Menu to login")
		
