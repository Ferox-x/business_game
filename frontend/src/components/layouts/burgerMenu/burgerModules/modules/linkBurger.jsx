import React from "react"
import "../burgerStyles/linkCoordinatorAttribute.scss"
import { useNavigate } from "react-router-dom"

function LinkBurger({ text, icon, url }) {
	const navigate = useNavigate()

	function redirectToUrl() {
		navigate(url)
	}

	return (
		<div className={"link_coordinator_container"} onClick={redirectToUrl}>
			<div className="link_coordinator_content">
				<div className={"link_coordinator_icon " + icon}></div>
				<p className="link_coordinator_value">{text}</p>
			</div>
			<div className="link_coordinator_enter"></div>
		</div>
	)
}

export default LinkBurger
