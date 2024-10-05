from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from ..db import get_session
from ..modelo.ticket import Ticket
from ..modelo.usuario import Usuario
from datetime import datetime

router = APIRouter(
    prefix="/incidentes",
    tags=["incidentes"],
)


@router.get("/tickets")
def obtener_tickets(session: Session = Depends(get_session)):
    tickets = session.exec(select(Ticket)).all()
    return tickets


@router.post("/tickets")
def crear_ticket(ticket: Ticket, session: Session = Depends(get_session)):
    ticket.id = None
    ticket.fecha_de_alta = datetime.now()

    usuario = session.exec(
        select(Usuario).where(Usuario.id == ticket.id_usuario)
    ).first()
    if not usuario:
        raise HTTPException(
            status_code=404, detail=f"Usuario con id {ticket.id_usuario} no existe"
        )

    session.add(ticket)
    session.commit()
    session.refresh(ticket)
    return ticket
