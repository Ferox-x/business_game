import React from "react"
import { useNavigate } from "react-router-dom"
import styles from "../../../generic/profileGenericStyles/userInfo.module.scss"
import { useSelector } from "react-redux"
import { urls } from "../../../../../urls"

function UserInfoCoordinator({ fontColor, ...props }) {
	const navigate = useNavigate()
	const user = useSelector((state) => state.user)

	let fullName = "Фамилия Имя"

	if (user.user.first_name && user.user.last_name) {
		fullName = user.user.first_name + " " + user.user.last_name
	}

	let fontColorClass = styles.user_info__color_white
	let fontPurpleColorClass = styles.user_info__color_white
	if (fontColor === "black") {
		fontColorClass = styles.user_info__color_black
		fontPurpleColorClass = styles.user_info__color_purple
	}

	function RedirectToEdit() {
		if (user.isCoordinator) {
			navigate(urls.profileCoordinatorEdit)
		}
	}

	return (
		<div className={[styles.user_info, fontColorClass].join(" ")}>
			<p className={[styles.user_name, fontColorClass].join(" ")}>{fullName}</p>
			<a
				href={"mailto:" + user.user.email}
				className={[styles.user_link_email, fontColorClass].join(" ")}
			>
				{user.user.email}
			</a>
			<div
				className={[styles.user_link_edit, fontPurpleColorClass].join(" ")}
				onClick={() => {
					RedirectToEdit()
				}}
			>
				Редактировать профиль
			</div>
		</div>
	)
}

export default UserInfoCoordinator
