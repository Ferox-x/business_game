import React, { useEffect, useState } from "react"
import Input from "../../../../components/UI-UX/input"
import Button from "../../../../components/UI-UX/button"
import Authentication from "./../../api/authorization"
import { useDispatch } from "react-redux"
import { useNavigate } from "react-router-dom"

function RegistrationForm({ code, ...props }) {
	const dispatch = useDispatch()
	const navigate = useNavigate()

	const [email, setEmail] = useState("")
	const [password, setPassword] = useState("")
	const [password2, setPassword2] = useState("")
	const [inviteCode, setInviteCode] = useState("")

	function signup() {
		new Authentication(dispatch)
			.registration(email, password, inviteCode)
			.then((response) => {
				if (response.status === 201) {
					navigate("/login")
				}
			})
	}

	useEffect(() => {
		if (code) {
			setInviteCode(code)
		}
	}, [])

	return (
		<form className={"auth_form"}>
			<div className="form_auth-inputs form_auth-input-registration">
				<Input
					type="email"
					placeholder="Почта"
					image="email"
					value={email}
					setValue={setEmail}
				/>
				<Input
					type="password"
					placeholder="Пароль"
					image="password"
					value={password}
					setValue={setPassword}
				/>
				<Input
					type="password"
					placeholder="Введите пароль ещё раз"
					image="password2"
					value={password2}
					setValue={setPassword2}
				/>
				<Input
					type="text"
					placeholder="Пригласительный код"
					image="invite_code"
					value={inviteCode}
					setValue={setInviteCode}
				/>
			</div>
			<div className="button_container">
				<Button action={() => signup()} children="Регистрация" />
			</div>
		</form>
	)
}

export default RegistrationForm
