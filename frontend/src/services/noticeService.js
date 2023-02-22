export class NoticeService {
	#infoStatus = "info"
	#errorStatus = "error"

	constructor(dispatch) {
		this.dispatch = dispatch
	}

	deleteNotice(noticeID) {
		this.dispatch({
			type: "DELETE_NOTICE",
			payload: { noticeID },
		})
	}

	addInfoNotice(message) {
		const notice = NoticeService.#createNoticeObject(1, message, this.#infoStatus)
		this.#addNotice(notice)
	}

	addErrorNotice(message) {
		const notice = NoticeService.#createNoticeObject(1, message, this.#errorStatus)
		this.#addNotice(notice)
	}

	#addNotice(noticeObject) {
		this.dispatch({
			type: "ADD_NOTICE",
			payload: noticeObject,
		})
		setTimeout(() => {
			this.deleteNotice(noticeObject.id)
		}, 5000)
	}

	static #createNoticeObject(id, message, status) {
		return {
			id: id,
			message: message,
			status: status,
		}
	}
}
