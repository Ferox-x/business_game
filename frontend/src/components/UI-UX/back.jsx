import React from "react"
import "./styles/back.scss"

import back from "../../static/img/back.svg"
import { useNavigate } from "react-router-dom"
import { urls } from "../../urls"

function Back({ url, ...props }) {
	const navigate = useNavigate()

	function redirectToProfile() {
		navigate(url)
	}

	return (
		<div onClick={() => redirectToProfile()} className={"button_back"}>
			<img src={back} alt="Back Button" />
		</div>
	)
}

export default Back
