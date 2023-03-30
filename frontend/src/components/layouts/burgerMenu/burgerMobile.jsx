import React from "react"
import { useSelector } from "react-redux"
import CoordinatorBurgerMobile from "./burgerModules/coordinatorBurgerMobile/coordinatorBurgerMobile"
import "../styles/burgerMobile.scss"
import PlayerBurgerMobile from "./burgerModules/playerBurgerMobile/playerBurgerMobile"

function BurgerMobile({ burgerState, hide }) {
	const user = useSelector((state) => state.user)

	let burgerStateClass

	switch (burgerState) {
		case false:
			burgerStateClass = "popup_hidden"
			break
		case true:
			burgerStateClass = "popup_open"
			break
	}

	let children = <></>

	if (user.isCoordinator) {
		children = <CoordinatorBurgerMobile hide={hide} />
	}

	if (user.isPlayer) {
		children = <PlayerBurgerMobile />
	}

	return <div className={"burger " + burgerStateClass}>{children}</div>
}

export default BurgerMobile
