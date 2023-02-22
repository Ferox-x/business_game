import React from "react"

import logo from "../../static/img/header/Logo.svg"
import { useNavigate } from "react-router-dom"
import { urls } from "../../urls"

function Logo({ className, ...props }) {
	const navigate = useNavigate()

	function redirectToMainPage() {
		navigate(urls.mainPage)
	}

	return (
		<img
			onClick={redirectToMainPage}
			className={className}
			src={logo}
			alt="Лого"
			{...props}
		/>
	)
}

export default Logo
