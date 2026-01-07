from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.buses.route import router as buses_router
from src.stops.route import router as stops_router
from src.bus_routes.route import router as bus_routes_router
from src.trips.route import router as trips_router
from src.drivers.route import router as drivers_router
from src.students.route import router as students_router
from src.admins.route import router as admins_router
from src.bus_locations.route import router as bus_locations_router


def create_app() -> FastAPI:
    app = FastAPI(title="AAU Bus Tracking API")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(buses_router)
    app.include_router(stops_router)
    app.include_router(bus_routes_router)
    app.include_router(trips_router)
    app.include_router(drivers_router)
    app.include_router(students_router)
    app.include_router(admins_router)
    app.include_router(bus_locations_router)
    from src.auth.route import router as auth_router
    app.include_router(auth_router)

    # Ensure DB tables are created after all table definitions are imported
    from src.database.connection import engine, metadata
    from src.database import schema as db_schema  # noqa: F401 - import side-effects
    metadata.create_all(bind=engine)

    @app.get("/health")
    def health():
        return {"status": "ok"}

    @app.get("/")
    def root():
        return {"app": "AAU Bus Tracking API", "docs": "/docs", "health": "/health"}

    return app


app = create_app()
