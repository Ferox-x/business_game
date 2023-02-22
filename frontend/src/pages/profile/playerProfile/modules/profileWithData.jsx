import React from "react"
import "../../generic/profileGenericStyles/profileFill.scss"
import FullName from "../../generic/components/fullName"
import PlayerAttributeList from "./playerAttributeList"
import UserInfo from "../../generic/components/userInfo"
import Layout from "../../../../components/layouts/layout"

function ProfileWithData({ data, ...props }) {
	return (
		<Layout>
			<div className="user_profile_data">
				<div className="user_info_container">
					<UserInfo fontColor={"black"} />
				</div>
				<div className="user_full_name_container">
					<FullName />
				</div>
				<div className="user_attribute_container">
					<PlayerAttributeList attributes={data} />
				</div>
			</div>
		</Layout>
	)
}

export default ProfileWithData
