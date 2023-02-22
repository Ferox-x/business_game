import React, { useState } from "react"
import "../recoveryPassword.scss"
import Input from "../../../../components/UI-UX/input"
import Button from "../../../../components/UI-UX/button"
import Authentication from "./../../api/authorization"

function RecoveryPasswordForm(props) {
	const [email, setEmail] = useState("")

	return (
		<form className={"recovery_password_form"}>
			<Input
				type="email"
				placeholder="Почта"
				value={email}
				setValue={setEmail}
				image="email"
			/>
			<div className="button_container">
				<Button action={() => Authentication.login(email)} children="Войти" />
			</div>
		</form>
	)
}

export default RecoveryPasswordForm
