from fastapi import FastAPI, Depends, status, HTTPException, Request, File, UploadFile
import pandas as pd
from database import engine, get_db
import models
from schemas import UserDetails, StageOne, StageTwo, StageThree
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI()

templates = Jinja2Templates(directory="templates/")

models.Base.metadata.create_all(bind=engine)


@app.get('/upload_csv', response_class=HTMLResponse)
def read_csv(request: Request):
    return templates.TemplateResponse("upload_csv.html", {"request": request})


@app.post('/submit_csv')
def handle_csv(csvfile: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        df = pd.read_csv(csvfile.file)
        for index, row in df.iterrows():
            if db.query(models.StudentTable).filter(models.StudentTable.email_id == row.email_id).first():
                pass
            else:
                engine.execute(
                    "INSERT INTO "
                    "demo_fastapi.students(full_name,email_id,graduation_completed,stream,cgpa,entrance_exam_score)"
                    "VALUES (%s, %s, %s, %s, %s, %s)",
                    row.full_name, row.email_id, row.graduation_completed, row.stream, row.cgpa,
                    row.entrance_exam_score)
        return "CSV uploaded successfully"
    except Exception as e:
        return e


@app.get('/add_details', response_class=HTMLResponse)
def read(request: Request):
    return templates.TemplateResponse("add_details.html", {"request": request})


@app.post('/details_added', status_code=status.HTTP_201_CREATED, response_class=HTMLResponse)
def add_details(form_data: UserDetails = Depends(UserDetails.as_form), db: Session = Depends(get_db)):
    new_details = models.StudentTable(full_name=form_data.full_name,
                                      email_id=form_data.email_id,
                                      graduation_completed=form_data.graduation_completed,
                                      stream=form_data.stream, cgpa=form_data.cgpa,
                                      entrance_exam_score=form_data.entrance_exam_score)
    db.add(new_details)
    db.commit()
    db.refresh(new_details)
    return "Data added successfully"


@app.get('/get_details')
def get_details(db: Session = Depends(get_db)):
    get_data = db.query(models.StudentTable).all()
    return get_data


@app.get('/stage_one', response_class=HTMLResponse)
def read_stage_one(request: Request):
    return templates.TemplateResponse("stage_one.html", {"request": request})


@app.post('/stage_one')
def grad_complete(request: Request, form_details: StageOne = Depends(StageOne.as_form), db: Session = Depends(get_db)):
    try:
        if form_details.graduation_completed == 'both':
            details = db.query(models.StudentTable).filter(
                models.StudentTable.graduation_completed.in_(['yes', 'no'])).all()

            db.query(models.StageOneTable).delete()
            db.commit()

            for detail in details:

                if db.query(models.StageOneTable).filter(models.StageOneTable.email_id == detail.email_id).first():
                    pass
                else:
                    new_details = models.StageOneTable(id=detail.id,
                                                       full_name=detail.full_name,
                                                       email_id=detail.email_id,
                                                       graduation_completed=detail.graduation_completed,
                                                       stream=detail.stream, cgpa=detail.cgpa,
                                                       entrance_exam_score=detail.entrance_exam_score)

                    db.add(new_details)
                    db.commit()
                    db.refresh(new_details)

            return templates.TemplateResponse("stage_one.html", {"request": request, "details": details})

        details = db.query(models.StudentTable).filter(
            models.StudentTable.graduation_completed == form_details.graduation_completed).all()
        if not details:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'That type of data is not present')

        db.query(models.StageOneTable).delete()
        db.commit()
        for detail in details:
            if db.query(models.StageOneTable).filter(models.StageOneTable.email_id == detail.email_id).first():
                pass
            else:
                new_details = models.StageOneTable(id=detail.id,
                                                   full_name=detail.full_name,
                                                   email_id=detail.email_id,
                                                   graduation_completed=detail.graduation_completed,
                                                   stream=detail.stream, cgpa=detail.cgpa,
                                                   entrance_exam_score=detail.entrance_exam_score)

                db.add(new_details)
                db.commit()
                db.refresh(new_details)

        return templates.TemplateResponse("stage_one.html", {"request": request, "details": details})

    except HTTPException as e:
        return e


@app.get('/stage_two', response_class=HTMLResponse)
def read_stage_two(request: Request):
    return templates.TemplateResponse("stage_two.html", {"request": request})


@app.post('/stage_two')
def check_stream(request: Request, form_details: StageTwo = Depends(StageTwo.as_form), db: Session = Depends(get_db)):
    # print(form_details.stream)
    details = db.query(models.StageOneTable).filter(models.StageOneTable.stream.in_(form_details.stream)).all()
    db.query(models.StageTwoTable).delete()
    db.commit()

    for detail in details:
        if db.query(models.StageTwoTable).filter(models.StageTwoTable.email_id == detail.email_id).first():
            pass
        else:
            new_details = models.StageTwoTable(id=detail.id,
                                               full_name=detail.full_name,
                                               email_id=detail.email_id,
                                               graduation_completed=detail.graduation_completed,
                                               stream=detail.stream, cgpa=detail.cgpa,
                                               entrance_exam_score=detail.entrance_exam_score)

            db.add(new_details)
            db.commit()
            db.refresh(new_details)
    return templates.TemplateResponse("stage_two.html", {"request": request, "details": details})


@app.get('/stage_three', response_class=HTMLResponse)
def read_stage_three(request: Request):
    return templates.TemplateResponse("stage_three.html", {"request": request})


@app.post('/stage_three')
def check_cgpa(request: Request, form_details: StageThree = Depends(StageThree.as_form), db: Session = Depends(get_db)):
    # print(form_details.cgpa_one,form_details.cgpa_two)
    details = db.query(models.StageTwoTable).filter(
        models.StageTwoTable.cgpa.between(cleft=form_details.cgpa_one, cright=form_details.cgpa_two)).all()
    # return details
    db.query(models.StageThreeTable).delete()
    db.commit()

    for detail in details:
        if db.query(models.StageThreeTable).filter(models.StageThreeTable.email_id == detail.email_id).first():
            pass
        else:
            new_details = models.StageThreeTable(id=detail.id,
                                                 full_name=detail.full_name,
                                                 email_id=detail.email_id,
                                                 graduation_completed=detail.graduation_completed,
                                                 stream=detail.stream, cgpa=detail.cgpa,
                                                 entrance_exam_score=detail.entrance_exam_score)

            db.add(new_details)
            db.commit()
            db.refresh(new_details)
    return templates.TemplateResponse("stage_three.html", {"request": request, "details": details})
