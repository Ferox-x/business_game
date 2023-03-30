import React, { useState } from "react"
import "./styles/burger_menu.css"
import burger_menu from "../../static/img/header/burger-menu.svg"
import Burger from "../layouts/burgerMenu/burger"
import { useChangeDisplay } from "../../pages/businessGame/hooks/hooks"

function BurgerMenu(props) {
	const [display, changeDisplay] = useChangeDisplay(false)

	return (
		<>
			<button className="menu_burger btn-reset">
				<img
					onClick={changeDisplay}
					src={burger_menu}
					alt="Menu"
					className={"menu_burger_icon"}
				/>
			</button>
			<Burger burgerState={display} hide={changeDisplay} />
		</>
	)
}

export default BurgerMenu
