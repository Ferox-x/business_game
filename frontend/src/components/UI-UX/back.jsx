import React from "react"
import "./styles/back.scss"
import sprite from "../../static/img/sprite.svg"
import { useNavigate } from "react-router-dom"
import { getIconFromSprite } from "../../utilits/utility"

function Back({ url, ...props }) {
	const navigate = useNavigate()

	function redirectToProfile() {
		navigate(url)
	}

	return (
		<div onClick={() => redirectToProfile()} className={"button_back"}>
			{getIconFromSprite(sprite, "back", 17, 30, "red")}
		</div>
	)
}

export default Back
