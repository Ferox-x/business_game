import { NoticeService } from "../services/noticeService"
import { getAxiosInstanceAuth } from "../actions/axios_config"

export class NoticeApiBase {
	constructor(dispatch) {
		this.dispatch = dispatch
	}
	createNoticeSuccess(message) {
		return new NoticeService(this.dispatch).addInfoNotice(message)
	}

	createNoticeError(errors) {
		errors.map((message, index) => {
			return new NoticeService(this.dispatch).addErrorNotice(message)
		})
	}
}

export class ChangePassword extends NoticeApiBase {
	changePassword(data) {
		const axios = getAxiosInstanceAuth()
		return axios
			.post("api/change-password", data)
			.then((response) => {
				this.createNoticeSuccess("Данные успешно обновлены")
			})
			.catch((response) => {
				const errors = response.response.data.errors
				this.createNoticeError(errors)
			})
	}
}
