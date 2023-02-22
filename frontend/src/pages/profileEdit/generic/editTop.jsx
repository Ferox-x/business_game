import React from "react"
import "../modules/editStyles/editTop.scss"
import Back from "../../../components/UI-UX/back"
import { urls } from "../../../urls"
import { useSelector } from "react-redux"

function EditTop({ attributesAndValue, fullName, sendForm, ...props }) {
	const user = useSelector((state) => state.user)

	let url

	if (user.isCoordinator) {
		url = urls.profileCoordinator
	}

	if (user.isPlayer) {
		url = urls.profilePlayer
	}

	return (
		<div className="edit_top">
			<Back url={url} />
			<button
				onClick={(event) => {
					event.preventDefault()
					sendForm()
				}}
				className="edit_completed btn-reset"
				type={"submit"}
			>
				Готово
			</button>
		</div>
	)
}

export default EditTop
