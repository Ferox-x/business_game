import React from "react"
import "./createGameStyles/inputSearch.scss"
import search from "../../../static/img/create_game/search.svg"

function InputSearch(props) {
	return (
		<div className={"search_form"}>
			<input type="search" placeholder={"Поиск"} className="input_search" />
			<button className={"search_form_btn btn_reset"} type="submit">
				<img className={"search_form_image"} src={search} alt="Search" />
			</button>
		</div>
	)
}

export default InputSearch
