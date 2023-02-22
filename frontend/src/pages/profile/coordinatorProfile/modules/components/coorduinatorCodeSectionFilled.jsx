import React, { useEffect, useState } from "react"
import "./coordinatorComponentsStyle/coordinatorCodeSection.scss"
import CoordinatorCode from "./coordinatorCode"
import CoordinatorUrl from "./coordinatorUrl"
import { CoordinatorInfo } from "../../../api/coordinatorProfileApi"
import { useDispatch } from "react-redux"

function CoordinatorCodeSectionFill(props) {
	const dispatch = useDispatch()

	const [inviteCode, setInviteCode] = useState("")

	function getCode() {
		new CoordinatorInfo(dispatch).getInviteCode().then((response) => {
			setInviteCode(response.data.invite_code)
		})
	}

	function updateInviteCode() {
		new CoordinatorInfo(dispatch).updateInviteCode().then((response) => {
			setInviteCode(response.data.invite_code)
		})
	}

	useEffect(() => {
		getCode()
	}, [])

	return (
		<div className={"coordinator_code_section_fill"}>
			<CoordinatorCode code={inviteCode} update={updateInviteCode} />
			<CoordinatorUrl code={inviteCode} />
		</div>
	)
}

export default CoordinatorCodeSectionFill
