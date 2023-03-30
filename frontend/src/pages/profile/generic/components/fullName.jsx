import React from "react"
import "../profileGenericStyles/fullName.scss"
import { useSelector } from "react-redux"

function FullName(props) {
	const user = useSelector((state) => state.user.user)
	return (
		<>
			<p className="user_full_name">
				{user.last_name + " " + user.first_name + " " + user.patronymic}
			</p>
		</>
	)
}

export default FullName
