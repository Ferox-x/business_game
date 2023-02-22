import { getAxiosInstanceAuth } from "../../../actions/axios_config"
import { ChangePassword, NoticeApiBase } from "../../../utilits/baseApiClasses"

export class PlayerProfileApi extends NoticeApiBase {
	async getAttributes() {
		const axiosInstanceAuth = getAxiosInstanceAuth()
		return await axiosInstanceAuth.get("api/player/attributes").then((response) => {
			if (response.status === 200) {
				return response.data
			}
		})
	}

	async setAttributes(data) {
		const axiosInstanceAuth = getAxiosInstanceAuth()
		return await axiosInstanceAuth
			.post("api/player/attributes", {
				attributes: { ...data },
			})
			.then((response) => {
				if (response.status === 200) {
					return true
				}
			})
			.catch((response) => {
				return response
			})
	}

	async setFullName(fullName) {
		const axiosInstanceAuth = getAxiosInstanceAuth()
		return await axiosInstanceAuth
			.post("api/player/retrieve", {
				...fullName,
			})
			.then((response) => {
				if (response.status === 200) {
					return response
				}
			})
			.catch((response) => {
				return response
			})
	}

	async sendForm(data) {
		let errors = []
		let fullNameErrors
		let attributeErrors
		try {
			fullNameErrors = (await this.setFullName(data.fullName)).response.data.errors
		} catch (TypeError) {}

		try {
			attributeErrors = (await this.setAttributes(data.attributesAndValue)).response
				.data.errors
		} catch (TypeError) {}

		if (attributeErrors) {
			errors.push(attributeErrors)
		}
		if (fullNameErrors) {
			errors.push(fullNameErrors)
		}
		if (errors.length !== 0) {
			this.createNoticeError(errors)
		} else {
			this.createNoticeSuccess("Данные успешно изменены.")
		}
	}
}
