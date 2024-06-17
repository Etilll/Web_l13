from typing import Annotated
from fastapi import APIRouter, HTTPException, Path, Depends, Query
from ..database.db import get_db
from ..schemas import ResponseContact, PostContact
from ..repository import contacts as contact_funcs
from ..database.models import User
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from ..services.auth import auth_service
from fastapi_limiter.depends import RateLimiter

router = APIRouter(prefix="/contacts", tags=["contacts"])

@router.get("/", response_model=list[ResponseContact], description='No more than 10 requests per minute', dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def all_contacts(skip: int = 0, limit: int = 100, curr_user: User = Depends(auth_service.get_current_user), db: Session=Depends(get_db), 
                    id: Annotated[int | None, Query(alias="id", example="id=42")]=None,
                    name: Annotated[str | None, Query(alias="name", example="name=Jone")]=None, 
                    surname: Annotated[str | None, Query(alias="surname", example="surname=Jenkins")]=None, 
                    mail: Annotated[str | None, Query(alias="mail", example="mail=123@gmail.com")]=None, 
                    phone: Annotated[str | None, Query(alias="phone", example="phone=380731290102")]=None):
    response = await contact_funcs.get_contacts(user=curr_user,db=db,id=id,name=name,surname=surname,mail=mail,phone=phone)
    if response == []:
        raise HTTPException(status_code=404, detail="No match was found, or the database is empty!")
    else:
        return response


@router.post("/", description='Should not add more that 5 contacts per minute', dependencies=[Depends(RateLimiter(times=5, seconds=60))])
async def add_contact(contact: PostContact, curr_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    response = await contact_funcs.add_contact(user=curr_user,contact=contact,db=db)
    if type(response) == IntegrityError:
        raise HTTPException(status_code=409, detail="Object with this id already exists in the system!")
    else:
        return response

@router.delete("/{contact_id}", description='Should not delete more that 5 contacts per minute', dependencies=[Depends(RateLimiter(times=5, seconds=60))])
async def del_contact(contact_id: Annotated[int, Path(title="The id of a contact to delete")], curr_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    response = await contact_funcs.delete_contact(user=curr_user,contact_id=contact_id, db=db)
    if response:
        return response
    else:
        raise HTTPException(status_code=404, detail="No specified contact was found!")

@router.put("/{contact_id}", description='Should not edit more that 5 contacts per minute', dependencies=[Depends(RateLimiter(times=5, seconds=60))])
async def put_contact(contact_id: Annotated[int, Path(title="The id of a contact to delete")], curr_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db), 
                    id: Annotated[int | None, Query(alias="id", example="id=42")]=None,
                    name: Annotated[str | None, Query(alias="name", example="name=Jone")]=None, 
                    surname: Annotated[str | None, Query(alias="surname", example="surname=Jenkins")]=None, 
                    mail: Annotated[str | None, Query(alias="mail", example="mail=123@gmail.com")]=None, 
                    phone: Annotated[str | None, Query(alias="phone", example="phone=380731290102")]=None): 
    response = await contact_funcs.put_contact(user=curr_user,contact_id=contact_id, id=id, name=name, surname=surname, mail=mail, phone=phone, db=db)
    if response:
        return response
    else:
        raise HTTPException(status_code=404, detail="No specified contact was found!")

@router.get("/bdays", description='Should not update birthday list more than two times per minute', dependencies=[Depends(RateLimiter(times=2, seconds=60))])
async def calc_birthdays(curr_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    response = await contact_funcs.calculate_birthdays(user=curr_user,db=db)
    return response
