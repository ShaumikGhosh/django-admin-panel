from django import forms


class AdminLoginForm(forms.Form):

    userCt = forms.CharField(
        widget = forms.TextInput(attrs={
            'class':'form-control',
            'id' : 'inputEmail',
            'placeholder' : 'Username / E-mail'
        })
    )

    password = forms.CharField(
        widget = forms.PasswordInput(attrs={
            'class' : 'form-control',
            'id': 'inputPassword',
            'placeholder' : 'Admin Password'
        })
    )

    remember_me = forms.BooleanField(
        required=False,
        label="Remember login for next time",
        widget = forms.CheckboxInput()
    )

    def clean_userCt(self):
        userCt = self.cleaned_data.get('userCt', None)
        if userCt.__eq__(""):
            msg = "Username / E-mail is required!"
            raise forms.ValidationError(msg)
        return userCt

    def clean_password(self):
        password = self.cleaned_data.get('password', None)
        if password.__eq__(""):
            msg = "Admin password is required!"
            raise forms.ValidationError(msg)
        return password


class ChangePasswordForm(forms.Form):

    oldPassword = forms.CharField(
        label = "Old password",
        required = False,
        widget = forms.PasswordInput(attrs={
            "placeholder" : "Enter old password",
            "class" : "form-control form-control-sm",
            "id" : "old-password",
        })
    )

    newPassword = forms.CharField(
        label = "New Password",
        required = False,
        widget = forms.PasswordInput(attrs={
            "placeholder" : "Enter new password",
            "class" : "form-control form-control-sm",
            "id" : "new-password",
        })
    )

    confirmPassword = forms.CharField(
        label = "Confirm Password",
        required = False,
        widget = forms.PasswordInput(attrs={
            "placeholder" : "Enter new password",
            "class" : "form-control form-control-sm",
            "id" : "confirm-password"
        })
    )

    def clean_oldPassword(self):
        oldPassword = self.cleaned_data.get("oldPassword", None)
        if oldPassword.__eq__(""):
            msg = "Old password is required!"
            raise forms.ValidationError(msg)
        return oldPassword

    def clean_newPassword(self):
        newPassword = self.cleaned_data.get("newPassword", None)
        if newPassword.__eq__(""):
            msg = "New password is required!"
            raise forms.ValidationError(msg)
        if len(newPassword) <=7:
            msg = "Password should not be less than 8 chars!"
            raise forms.ValidationError(msg)
        return newPassword

    def clean_confirmPassword(self):
        confirmPassword = self.cleaned_data.get("confirmPassword", None)
        if confirmPassword.__eq__(""):
            msg = "Confirm password is required!"
            raise forms.ValidationError(msg)
        if len(confirmPassword) <=7:
            msg = "Password should not be less than 8 chars!"
            raise forms.ValidationError(msg)
        return confirmPassword

    def clean(self):
        cleanedData = super(ChangePasswordForm, self).clean()
        newPassword = cleanedData.get('newPassword', None)
        confirmPassword = cleanedData.get("confirmPassword", None)

        if newPassword.__ne__(confirmPassword):
            msg = "New password didn't match to Confirm Password"
            raise forms.ValidationError(msg)
        return cleanedData



SELECT_ACTIONS = (
    ('', '-- Select Action --'),
    ('activate', 'Activate All User'),
    ('deactivate', 'Deactivate All User'),
    ('delete', 'Delete Selected'),
    ('do_superuser', 'Do Superuser Selected'),
    ('undo_superuser', 'Undo Superuser Selected'),
)

class UserActionForm(forms.Form):

    selectAction = forms.CharField(
        required=False,
        widget= forms.Select(attrs={'id':'select-action', 'style':"margin-bottom: 5px;"}, choices=SELECT_ACTIONS)
    )

    def clean_selectAction(self):
        selectAction = self.cleaned_data.get('selectAction', None)
        if selectAction.__eq__(""):
            raise forms.ValidationError("Operation type is required")
        return selectAction