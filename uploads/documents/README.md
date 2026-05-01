# Ampalone Partner Portal

## AI-Powered Enterprise Security Partner Management System

**Version:** 1.0.0  
**Last Updated:** January 2026  
**Company:** Ampalone Softwares Private Limited  
**CIN:** U72200KA2020PTC134567

---

## Overview

The Ampalone Partner Portal is a comprehensive partner management system for Ampalone's AI-powered enterprise security products including DocXsyn AI, Netrix, and Orbit Endpoint.

### Key Features

- **Partner Registration** - Complete onboarding with Indian compliance (PAN, GST, CIN)
- **Customer Management** - Tag and manage prospects/customers
- **Quotation Generation** - Create quotations with discount approval workflow
- **Document Management** - Download NDA, MSA, SLA
- **Analytics Dashboard** - Pipeline tracking and performance metrics
- **Admin Panel** - Pricing management and approval workflows

---

## Technology Stack

| Component | Technology |
|-----------|------------|
| Backend | Python 3.11 + FastAPI |
| Database | PostgreSQL 15 |
| Cache | Redis 7 |
| Authentication | JWT + OAuth2 |
| PDF Generation | ReportLab |
| Container | Docker + Docker Compose |

---

## Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL 15+
- Redis 7+
- Docker (optional)

### Installation

```bash
# Clone repository
git clone https://github.com/ampalone/partner-portal.git
cd partner-portal

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env
# Edit .env with your configuration

# Run database migrations
alembic upgrade head

# Start development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
