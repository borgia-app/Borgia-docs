## Permissions

### How they are created

Permissions in Borgia are automatically created for each model.

#### Default permissions
The default permissions are : add, change, delete, view.

To change the default permissions, one needs to override the default_permissions inside a Meta class inside the model class.

Example below, from Borgia :

```
class WeightsUser(models.Model):
    //-- some fields --//

    class Meta:
        """
        Remove default permissions for WeightsUser
        """
        default_permissions = ()
```

Here, all default permissions are removed.
In Borgia's code, you may also see :

`default_permissions = ('add', 'view',)`,

To only remove delete and change permissions.

#### Additionnal permissions

On top off default permissions, we can adcreate and add customs :

```
class Event(models.Model):
    """
    A shared event, paid by many users

    """
    //-- Fields --//
    class Meta:
        """
        Define Permissions for Event.

        :note:: Initial Django Permission (add, change, delete, view) are added.
        """
        permissions = (
            # CRUDL
            # add_event
            # change_event
            # delete_event
            # view_event
            ('self_register_event', 'Can self register to an event'),
            ('proceed_payment_event', 'Can proceed to payment for an event'),
        )
```

Here, we added two new permissions, 'self_register_event' and 'proceed_payment_event'. Each of them also has a small description, that is used to explain the goal of the permission in the UI, for the managers.

## Further read :

https://docs.djangoproject.com/en/4.2/topics/auth/default/#topic-authorization