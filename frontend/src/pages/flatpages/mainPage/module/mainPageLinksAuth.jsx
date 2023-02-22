import React from "react"
import { useNavigate } from "react-router-dom"
import { urls } from "../../../../urls"
import { useSelector } from "react-redux"

function MainPageLinksAuth(props) {
	const user = useSelector((state) => state.user)
	const navigate = useNavigate()

	function RedirectToProfile() {
		if (user.isPlayer) {
			navigate(urls.profilePlayer)
		}
		if (user.isCoordinator) {
			navigate(urls.profileCoordinator)
		}
	}

	function RedirectToLogOut() {
		navigate(urls.logout)
	}

	return (
		<div className="links_container">
			<div
				className="link_auth link_registration"
				onClick={() => {
					RedirectToProfile()
				}}
			>
				Профиль
			</div>
			<div
				className="link_auth link_login"
				onClick={() => {
					RedirectToLogOut()
				}}
			>
				Выход
			</div>
		</div>
	)
}

export default MainPageLinksAuth
