import React, { useState } from "react"
import "../generic/genericEditStyles/formPassword.scss"
import FormButton from "../generic/formButton"
import FormLabelPassword from "../components/formLabelPassword"
import { ChangePassword } from "../../../utilits/baseApiClasses"
import { useDispatch } from "react-redux"

function FormPassword(props) {
	const [oldPassword, setOldPassword] = useState("")
	const [newPassword, setNewPassword] = useState("")
	const [newPassword2, setNewPassword2] = useState("")

	const dispatch = useDispatch()

	function sendNewPassword() {
		new ChangePassword(dispatch).changePassword({
			old_password: oldPassword,
			new_password: newPassword,
			new_password2: newPassword2,
		})
	}

	return (
		<form className="form_password">
			<FormLabelPassword
				htmlFor={"old_password"}
				value={oldPassword}
				setValue={setOldPassword}
				label={"Старый пароль"}
				type={"password"}
				id={"old_password"}
				placeholder={"Старый пароль"}
			/>
			<FormLabelPassword
				htmlFor={"new_password"}
				value={newPassword}
				setValue={setNewPassword}
				label={"Новый пароль"}
				type={"password"}
				id={"new_password"}
				placeholder={"Новый пароль"}
			/>
			<FormLabelPassword
				htmlFor={"repeat_password"}
				value={newPassword2}
				setValue={setNewPassword2}
				label={"Подтвердите новый пароль"}
				type={"password"}
				id={"repeat_password"}
				placeholder={"Подтвердите новый пароль"}
			/>
			<FormButton action={sendNewPassword} children={"Изменить пароль"} />
		</form>
	)
}

export default FormPassword
