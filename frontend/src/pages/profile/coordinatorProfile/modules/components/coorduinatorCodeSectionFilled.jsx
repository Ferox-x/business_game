import React from "react"
import "./coordinatorComponentsStyle/coordinatorCodeSection.scss"
import { CoordinatorInfo } from "../../../api/coordinatorProfileApi"
import { useDispatch } from "react-redux"
import CodeSection from "../codeSection/codeSection"

function CoordinatorCodeSectionFill({ ...props }) {
	const dispatch = useDispatch()

	const coordinatorInfo = new CoordinatorInfo(dispatch)

	function getCode() {
		return coordinatorInfo.getInviteCode().then((response) => {
			return response
		})
	}

	function updateInviteCode() {
		return coordinatorInfo.updateInviteCode().then((response) => {
			return response
		})
	}

	return <CodeSection getCode={getCode} updateCode={updateInviteCode} />
}

export default CoordinatorCodeSectionFill
