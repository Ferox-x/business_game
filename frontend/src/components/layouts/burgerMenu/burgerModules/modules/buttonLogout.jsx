import React from "react"
import "../burgerStyles/buttonLogout.scss"
import { useNavigate } from "react-router-dom"
import { urls } from "../../../../../urls"

function ButtonLogout(props) {
	const navigate = useNavigate()

	function redirectToLogout() {
		navigate(urls.logout)
	}

	return (
		<button onClick={redirectToLogout} className={"btn_reset burger_button_logout"}>
			Выйти
		</button>
	)
}

export default ButtonLogout
