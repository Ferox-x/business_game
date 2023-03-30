import React, { useState } from "react"
import "../../../generic/profileGenericStyles/profileFill.scss"
import UserInfoCoordinator from "../components/userInfoCoordinator"
import FullName from "../../../generic/components/fullName"
import CoordinatorAttributeList from "../components/coordinatorAttributeList"
import CoordinatorCodeSectionFill from "../components/coorduinatorCodeSectionFilled"
import Popup from "../../../popup/popup"
import InviteButton from "../components/inviteButton"
import Layout from "../../../../../components/layouts/layout"

function CoordinatorWithData({ data, ...props }) {
	const [displayPopUp, setDisplayPopUp] = useState(0)

	function hidePopUp() {
		setDisplayPopUp(0)
	}

	function openPopUp() {
		setDisplayPopUp(1)
	}

	return (
		<Layout>
			<div className="user_profile_data">
				<div className="user_info_container">
					<UserInfoCoordinator fontColor={"black"} />
				</div>
				<div className="user_full_name_container">
					<FullName />
				</div>
				<div className="user_profile_data__code">
					<CoordinatorCodeSectionFill />
				</div>
				<div className="user_attribute_container">
					<CoordinatorAttributeList attributes={data} />
				</div>
				<div className="user_profile_data__btn">
					<InviteButton open={openPopUp} />
				</div>
			</div>
			<Popup popUpState={displayPopUp} hide={hidePopUp} />
		</Layout>
	)
}

export default CoordinatorWithData
