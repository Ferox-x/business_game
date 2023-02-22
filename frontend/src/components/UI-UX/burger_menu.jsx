import React, { useState } from "react"
import "./styles/burger_menu.css"
import burger_menu from "../../static/img/header/burger-menu.svg"
import Burger from "../layouts/burgerMenu/burger"

function BurgerMenu(props) {
	const [burgerDisplay, setBurgerDisplay] = useState(0)

	function hideBurger() {
		setBurgerDisplay(0)
	}

	function openBurger() {
		setBurgerDisplay(1)
	}

	return (
		<>
			<button className="menu_burger btn-reset">
				<img
					onClick={openBurger}
					src={burger_menu}
					alt="Menu"
					className={"menu_burger_icon"}
				/>
			</button>
			<Burger burgerState={burgerDisplay} hide={hideBurger} />
		</>
	)
}

export default BurgerMenu
