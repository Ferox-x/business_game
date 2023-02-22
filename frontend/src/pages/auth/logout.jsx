import React, { useEffect } from "react"
import { useDispatch } from "react-redux"
import { useNavigate } from "react-router-dom"
import { urls } from "../../urls"
import { NoticeService } from "../../services/noticeService"

function Logout(props) {
	const dispatch = useDispatch()
	const navigate = useNavigate()

	useEffect(() => {
		dispatch({
			type: "CLEAR_USER",
		})
		navigate(urls.mainPage)
		new NoticeService(dispatch).addInfoNotice("Вы успешно вышли.")
	}, [])

	return <></>
}

export default Logout
