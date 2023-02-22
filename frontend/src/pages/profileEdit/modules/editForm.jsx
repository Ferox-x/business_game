import React, { useState } from "react"
import "./editStyles/editForm.scss"
import FormFullName from "./formFullName"
import FormAttributes from "./formAttributes"
import EditTop from "../generic/editTop"
import { useDispatch, useSelector } from "react-redux"
import { PlayerProfileApi } from "../api/playerEditApi"
import { PlayerInfo } from "../../profile/api/playerProfileApi"

function EditForm(props) {
	const user = useSelector((state) => state.user)
	const dispatch = useDispatch()

	const [fullName, setFullName] = useState({
		first_name: user.user.first_name,
		last_name: user.user.last_name,
		patronymic: user.user.patronymic,
	})

	const [attributesAndValue, setAttributesAndValue] = useState({})

	function sendForm() {
		new PlayerProfileApi(dispatch).sendForm({ fullName, attributesAndValue })
		new PlayerInfo(dispatch).getPlayerInfo()
	}

	return (
		<form action={""} method={"Post"}>
			<EditTop
				attributesAndValue={attributesAndValue}
				fullName={fullName}
				sendForm={sendForm}
			/>
			<FormFullName fullName={fullName} setFullname={setFullName} />
			<FormAttributes
				attributesAndValue={attributesAndValue}
				setAttributesAndValue={setAttributesAndValue}
			/>
		</form>
	)
}

export default EditForm
