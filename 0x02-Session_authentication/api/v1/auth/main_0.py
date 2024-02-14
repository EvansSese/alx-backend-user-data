#!/usr/bin/env python3
""" Main 0
"""
import auth

a = auth.Auth()

print(a.require_auth("/api/v1/status/", ["/api/v1/status/"]))
print(a.authorization_header())
print(a.current_user())
