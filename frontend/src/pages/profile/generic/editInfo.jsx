import React from "react"
import profile_empty from "../../../static/img/profile/profile_empty.svg"
import "./profileGenericStyles/profileEmpty.scss"

function EditInfo(props) {
	return (
		<div className={"user_info_empty__container"}>
			<div className={"profile_empty"}>
				<img
					src={profile_empty}
					alt="Profile Empty Icon"
					className="profile_empty_image"
				/>
				<span className="profile_empty_text">
					Вы можете добавить информацию о себе в меню редактирования
				</span>
			</div>
		</div>
	)
}

export default EditInfo
