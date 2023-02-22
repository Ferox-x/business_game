import React from "react"
import "../../../generic/profileGenericStyles/profileFill.scss"
import "../../../generic/profileGenericStyles/profileEmpty.scss"
import UserInfoCoordinator from "../components/userInfoCoordinator"
import EditInfo from "../../../generic/editInfo"
import LayoutGradient from "../../../../../components/layouts/layoutGradient"

function CoordinatorWithOutData(props) {
	return (
		<LayoutGradient>
			<div className={"user_profile_empty"}>
				<div className="user_info_container">
					<UserInfoCoordinator />
				</div>
				<EditInfo />
			</div>
		</LayoutGradient>
	)
}

export default CoordinatorWithOutData
