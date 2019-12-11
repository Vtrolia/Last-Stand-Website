from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("account-settings", views.account_page, name="account_page"),
    path("create-cloud", views.create_cloud, name="create_cloud"),
    path("client-downloads", views.client_page, name="client_downloads"),
    path("issues", views.issue_page, name="issue_page"),
    path("license", views.license_page, name="license_page"),
    path("login", views.login_page, name="login_page"),
    path("logout", views.logout_user, name="logout_user"),
    path("more-info", views.more_info, name="more_info"),
    path("last-stand-cloud", views.last_stand_cloud_page, name="last_stand_cloud"),
    path("publish", views.publish_page, name="publish_page"),
    path("rates", views.rates, name="rates"),
    path("relog", views.relog_page, name="relog"),
    path("smart-ornament", views.smart_ornament, name="smart_ornament"),
    path("settings", views.settings, name="settings"),
    path("signup", views.register_page, name="register_page"),
    path("submit-article", views.submit_article, name="submit_article"),
    path("submit-login", views.submit_login, name="submit_login"),
    path("submit-issue", views.submit_issue, name="submit_issue"),
    path("submit-register", views.submit_register, name="submit_register"),
    path("add-name", views.add_name, name="add_name"),
    path("submit-application", views.submit_application, name="submit_publisher"),
    path("submit-details", views.submit_change, name="submit_change"),
    path("submit-delete-account", views.submit_delete_account, name="submit_delete_account"),
    path("submit-password-change", views.submit_password_change, name="submit_password_change"),
    path("get-articles", views.load_articles, name="load_articles"),
    path("stories", views.story, name="our_story"),
    path("load/<template>", views.load, name="load_template"),
    path("cloud-options-page", views.load_cloud_options, name="load_cloud_options"),
    path("base-options-page", views.load_base_options, name="load_base_options"),
    path("change-plan-page", views.load_change_plan, name="load_plan_page"),
    path("become-publisher", views.load_request_publisher, name="request_publisher")
    
]