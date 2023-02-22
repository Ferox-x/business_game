import React from "react"
import "../styles/header.scss"
import Logo from "../../UI-UX/logo"
import BurgerMenu from "../../UI-UX/burger_menu"

function Header({ capacity = true, ...props }) {
	let headerColorClassName = ""

	if (!capacity) {
		headerColorClassName = "header_purple"
	}

	return (
		<header className={"header " + headerColorClassName}>
			<div className="header_container">
				<BurgerMenu />
				<Logo className={"header_logo_container"} />
			</div>
		</header>
	)
}

export default Header
