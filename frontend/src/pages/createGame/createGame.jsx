import React, { useState } from "react"
import "./createGame.scss"
import InputNameGame from "./modules/inputNameGame"
import InputStartGame from "./modules/inputStartGame"
import CheckboxAttributeList from "./modules/checkboxAttributeList"
import InputSearch from "./modules/inputSearch"
import Button from "../../components/UI-UX/button"
import Layout from "../../components/layouts/layout"
import ButtonCreateGame from "../../components/layouts/burgerMenu/burgerModules/modules/buttonCreateGame"

function CreateGame(props) {
	const [gameName, setGameName] = useState("")

	const [requiredAttributes, setRequiredAttributes] = useState({})

	function changeRequiredAttributes(name, value) {
		let requiredObject = requiredAttributes
		requiredObject[name] = value
		setRequiredAttributes({ ...requiredObject })
	}

	console.log(requiredAttributes)

	return (
		<>
			<Layout />
			<div className="create_game_body">
				<div className="create_game_left">
					<InputNameGame value={gameName} setValue={setGameName} />
					<div className="start_game_container">
						<InputStartGame
							placeholder={"Не указано"}
							type={"time"}
							label={"Время старта игры"}
						/>
						<div className="button_create_game_container">
							<ButtonCreateGame children={"Создать игру"} />
							{/*<ButtonCreateGame children={"Создать игру"}*/}
							{/*                  style={{width: '400px'}}/>*/}
						</div>
					</div>
				</div>
				<div className="checkbox_attribute_list_container">
					<div className="input_search_container">
						<InputSearch />
					</div>
					<CheckboxAttributeList setValue={changeRequiredAttributes} />
				</div>
			</div>
		</>
	)
}

export default CreateGame
