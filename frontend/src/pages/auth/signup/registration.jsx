import React from "react"
import "./registration.scss"
import "../../genericStyles/_generic.scss"
import Title from "../../../components/UI-UX/title"
import HelpTextMessage from "../../../components/UI-UX/help_text_message"
import RegistrationForm from "./module/registrationForm"
import AuthPage100Vh from "../../flatpages/authpage100vh"
import { useParams } from "react-router-dom"

function Registration(props) {
	const { code } = useParams()

	return (
		<AuthPage100Vh>
			<div className="title_container">
				<Title title={"Добро пожаловать!"} />
			</div>
			<div className="form_auth">
				<RegistrationForm code={code} />
			</div>
			<HelpTextMessage link={"/login"} text="Войти" message="Уже есть аккаунт?" />
		</AuthPage100Vh>
	)
}

export default Registration
