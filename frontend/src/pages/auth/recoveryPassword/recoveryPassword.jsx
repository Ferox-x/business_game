import React from "react"
import "./recoveryPassword.scss"
import "../../genericStyles/_generic.scss"
import RecoveryPasswordForm from "./module/recoveryPasswordForm"
import HelpText from "../../../components/UI-UX/help_text"
import AuthPage100Vh from "../../flatpages/authpage100vh"

function RecoveryPassword(props) {
	return (
		<AuthPage100Vh>
			<p className="password_recovery_text">
				Пожалуйста, укажите почту, которую вы&nbsp;использовали для входа
			</p>
			<div className="form_auth">
				<RecoveryPasswordForm />
			</div>
			<HelpText link={"/login"} text={"Вернуться на страницу авторизации"} />
		</AuthPage100Vh>
	)
}

export default RecoveryPassword
