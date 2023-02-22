import React from "react"
import "../mainPage.scss"
import { useNavigate } from "react-router-dom"
import { urls } from "../../../../urls"

function MainPageLinks(props) {
	const navigate = useNavigate()

	function RedirectToSignUp() {
		navigate(urls.signUp)
	}

	function RedirectToLogin() {
		navigate(urls.login)
	}

	return (
		<div className="links_container">
			<div
				className="link_auth link_registration"
				onClick={() => {
					RedirectToSignUp()
				}}
			>
				Регистрация
			</div>
			<div
				className="link_auth link_login"
				onClick={() => {
					RedirectToLogin()
				}}
			>
				Войти
			</div>
		</div>
	)
}

export default MainPageLinks
