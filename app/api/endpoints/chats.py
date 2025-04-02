from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, WebSocket
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.websockets import WebSocketDisconnect

from app.api.schemas import MessageSchema, ChatSchema, PersonalChatCreateSchema, GroupChatCreateSchema
from app.core.containers import Container
from app.core.exceptions.not_found_exceptions import ChatNotFoundException
from app.core.managers import WebsocketManager
from app.core.services import ChatService

router = APIRouter()


@router.get('/{chat_id}')
@inject
async def websocket_chat(
    websocket: WebSocket,
    chat_id: int,
    ws_manager: WebsocketManager = Depends(Provide[Container.ws_manager]),
    chat_service: ChatService = Depends(Provide[Container.chat_service]),
    db_session: AsyncSession = Depends(Provide[Container.db_session])
):
    await ws_manager.connect(chat_id, websocket)
    try:
        while True:
            data = await websocket.receive_json()
            message = await chat_service.create_message(
                session=db_session,
                chat_id=chat_id,
                sender_id=data['sender_id'],
                text=data['text'],
            )
            message_data = {
                'id': message.id,
                'chat_id': message.chat_id,
                'sender_id': message.sender_id,
                'text': message.text,
                'timestamp': message.timestamp.isoformat(),
            }
            await ws_manager.send_message(chat_id, message_data)
    except ChatNotFoundException as e:
        await websocket.send_json({
            'detail': e.message
        })
    except WebSocketDisconnect:
        await ws_manager.disconnect(chat_id, websocket)
    except Exception:
        await websocket.close()


@router.get('/history/{chat_id}', response_model=list[MessageSchema])
@inject
async def get_chat_history(
    chat_id: int,
    chat_service: ChatService = Depends(Provide[Container.chat_service]),
    db_session: AsyncSession = Depends(Provide[Container.db_session])
):
    try:
        messages = await chat_service.get_chat_history(
            session=db_session,
            chat_id=chat_id,
        )
        return messages
    except ChatNotFoundException as exception:
        raise HTTPException(
            status_code=exception.status_code,
            detail=exception.message
        )
    except Exception:
        raise HTTPException(500, detail='Internal server error')


@router.post('/create_personal_chat', response_model=ChatSchema)
@inject
async def create_personal_chat(
    chat_data: PersonalChatCreateSchema,
    chat_service: ChatService = Depends(Provide[Container.chat_service]),
    db_session: AsyncSession = Depends(Provide[Container.db_session])
):
    try:
        await chat_service.create_personal_chat(
            session=db_session,
            chat_name=chat_data.name
        )
    except Exception:
        raise HTTPException(500, detail='Internal server error')


@router.post('/create_group_chat')
@inject
async def create_group_chat(
    chat_data: GroupChatCreateSchema,
    chat_service: ChatService = Depends(Provide[Container.chat_service]),
    db_session: AsyncSession = Depends(Provide[Container.db_session])
):
    try:
        await chat_service.create_group_chat(
            session=db_session,
            chat_name=chat_data.name,
            group_id=chat_data.group_id
        )
    except Exception:
        raise HTTPException(500, detail='Internal server error')
