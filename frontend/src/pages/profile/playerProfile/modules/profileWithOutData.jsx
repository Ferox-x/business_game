import React from "react"
import "../../generic/profileGenericStyles/profileEmpty.scss"

import UserInfo from "../../generic/components/userInfo"
import EditInfo from "../../generic/editInfo"
import LayoutGradient from "../../../../components/layouts/layoutGradient"

function ProfileWithOutData(props) {
	return (
		<LayoutGradient>
			<div className="user_info_container">
				<UserInfo />
			</div>
			<EditInfo />
		</LayoutGradient>
	)
}

export default ProfileWithOutData
