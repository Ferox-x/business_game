import React from "react"
import "./editFormCoordinatorStyles/editFormCoordinator.scss"
import FormAttributeCoordinator from "./formAttributeCoordinator"
import { useState } from "react"
import { useDispatch, useSelector } from "react-redux"
import FormFullNameCoordinator from "./formFullNameCoordinator"
import EditTop from "../../generic/editTop"
import { CoordinatorEditApi } from "../../api/coordinatorEditApi"
import { CoordinatorInfo } from "../../../profile/api/coordinatorProfileApi"

function EditFormCoordinator(props) {
	const user = useSelector((state) => state.user)
	const dispatch = useDispatch()

	const [fullName, setFullName] = useState({
		first_name: user.user.first_name,
		last_name: user.user.last_name,
		patronymic: user.user.patronymic,
	})

	const [attributesAndValue, setAttributesAndValue] = useState({})

	function sendForm() {
		new CoordinatorEditApi(dispatch).sendForm({ ...fullName, ...attributesAndValue })
		new CoordinatorInfo(dispatch).getCoordinatorInfo()
	}

	return (
		<form action={"#"} method={"POST"}>
			<EditTop
				attributesAndValue={attributesAndValue}
				fullName={fullName}
				sendForm={sendForm}
			/>
			<FormFullNameCoordinator fullName={fullName} setFullname={setFullName} />
			<FormAttributeCoordinator
				attributesAndValue={attributesAndValue}
				setAttributesAndValue={setAttributesAndValue}
			/>
		</form>
	)
}

export default EditFormCoordinator
