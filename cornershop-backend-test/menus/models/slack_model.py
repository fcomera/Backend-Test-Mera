"""This module contains the specification the model that abstracts
the methods required to process orders

NOTICE: This model is not stored in the database
"""
from employees.models.employee import Employee


class SlackModel:
    """This class implement static methods(class methods precisely) that
    process the incoming data when an Slack action is triggered."""

    @classmethod
    def process_body(cls, body):
        """This method obtains the ids of the selected option and
        the customization added by a user in an Slack action. This
        is in order to obtain the data in the future more easily.

        :param body: The body that contains the data from the
                     triggered action in Slack
        :type body: dict

        :return: A list of strings that represent the keys
                 in the body dictionary in order to obtain
                 the required values
        :rtype:  list
        """
        state = body['state']['values']
        inputs = [slack_input['block_id'] for slack_input in body['message']['blocks']][1:]
        values = [state[oi] for oi in inputs]
        return [ops[1] for ls in values for ops in ls.items()]

    @classmethod
    def process_values(cls, values):
        """This method creates a list from the values dictionary
        in order to deliver to this class the required values
        to register or update an order.

        :param values:  List containing the data required
                        to create or update an order
                        It can have the next format
                        [
                            {
                                'type': 'radio_buttons',
                                'selected_option': {
                                    'value': The value
                                },
                            },
                            {
                                'type': 'plain_text_input',
                                'value': The value
                            }
                        ]
        :type values: list of dictionaries

        :return: Return the list of dictionaries with the
                 values required to create or update and order
        :rtype: list
        """
        output = []
        for value in values:
            if value['type'] == 'radio_buttons':
                if value['selected_option']:
                    output.append(
                        {
                            'option': value['selected_option']['value']
                        }
                    )
                if not value['selected_option']:
                    raise NotSelectedOption
            if value['type'] == 'plain_text_input':
                output.append(
                    {
                        'customization': value['value']
                    }
                )
        return output

    @classmethod
    def get_dictionary_from_values(cls, user, values):
        """This method creates the dictionary that will create or
        update an order. It also adds to it the information
        of the user.

        :param user: Dictionary containing the information of
                     a slack user
        :type user: dict
        :param values: The values of the selected option and the
                        customization of an order.
        :type values: dict

        :return: Returns the dictionary that will be used to create
                 an order or update an existing order.
        :rtype: dict
        """
        values.append({
            'slack_user_id': user['id'],
            'username': user['username']
        })
        pos = {}
        [
            pos.update(val)
            for val in values
        ]
        return pos

    @classmethod
    def create_order(cls, body):
        """This method creates or updates an order with the data
        obtained by the slack action.

        :param body: The body of the action triggered in slack
        :type body: dict
        """
        user = body['user']
        pre_processed = cls.process_body(body)
        values = cls.process_values(pre_processed)
        data = cls.get_dictionary_from_values(user, values)
        Employee.objects.create_update_order(**data)
