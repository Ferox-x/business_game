import React from "react"
import "./login.scss"
import "../../genericStyles/_generic.scss"
import HelpTextMessage from "../../../components/UI-UX/help_text_message"
import Title from "../../../components/UI-UX/title"
import LoginForm from "./module/loginForm"
import AuthPage100Vh from "../../flatpages/authpage100vh"

function Login(props) {
	return (
		<AuthPage100Vh>
			<div className="title_container">
				<Title title={"Добро пожаловать!"} />
			</div>
			<div className="form_auth">
				<LoginForm />
			</div>
			<HelpTextMessage
				link={"/signup"}
				message={"Ещё нет аккаунта?"}
				text={"Регистрация"}
			/>
		</AuthPage100Vh>
	)
}

export default Login
