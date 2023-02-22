import React from "react"
import "./burgerStyles/coordinatorBurger.scss"
import LinksBurgerCoordinator from "./modules/linksBurgerCoordinator"
import ButtonLogout from "./modules/buttonLogout"
import ButtonCreateGame from "./modules/buttonCreateGame"

function CoordinatorBurger(props) {
	return (
		<>
			<div className={"burger_container_content"}>
				<div className={"burger_modal_content"}>
					<LinksBurgerCoordinator />
					<ButtonLogout />
				</div>
				<div className="button_create_game_container">
					<ButtonCreateGame children={"Создать игру"} />
				</div>
			</div>
		</>
	)
}

export default CoordinatorBurger
