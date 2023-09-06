@main.route("/<source>/update/single", methods=["POST"])
def contacts_update_single(source):
    if source not in Config.SOURCE_CONTACT:
        error = logger.error("No such collection in the database")
        return error

    print("New Update Request Received")
    request_id = str(request.form.get("request_id", "")).strip()
    party_role_id = str(request.form.get("party_role_id", "")).strip()
    first_name = str(request.form.get('first_name', "")).strip()
    last_name = str(request.form.get("last_name", "")).strip()
    mobile_num = str(request.form.get('mobile_number', "")).strip()
    mobile_num_ext = str(request.form.get("mobile_number_ext", "")).strip()
    direct_num = str(request.form.get('direct_number', "")).strip()
    direct_num_ext = str(request.form.get('direct_number_ext', "")).strip()
    home_num = str(request.form.get('home_number', "")).strip()
    home_num_ext = str(request.form.get('home_number_ext', "")).strip()
    business_email = str(request.form.get('business_email', "")).strip()
    personal_email = str(request.form.get('personal_email', "")).strip()
    other_email = str(request.form.get('other_email', "")).strip()
    website = str(request.form.get('website', "")).strip()

    if request_id == "":
        response = {
            "status": "Error",
            "request_id": request_id,
            "info": {
                "message": f"REQUEST_ID is required to complete the request",

            }
        }
        return jsonify(response)

    elif party_role_id == "":
        response = {
            "status": "Error",
            "request_id": request_id,
            "info": {
                "message": f"PARTYROLEID is required to complete the request",

            }
        }
        return jsonify(response)

    else:
        query = {'_id': party_role_id}
        update_request = {
            "_id": party_role_id,
            "PARTYROLEID": party_role_id,
            "FIRSTNAME": first_name,
            "LASTNAME": last_name,
            "MOBILE_NUMBER": mobile_num,
            "MOBILE_NUMBER_EXT": mobile_num_ext,
            "DIRECT_NUMBER": direct_num,
            "DIRECT_NUMBER_EXT": direct_num_ext,
            "HOME_NUMBER": home_num,
            "HOME_NUMBER_EXT": home_num_ext,
            "BUSINESS_EMAIL": business_email,
            "PERSONAL_EMAIL": personal_email,
            "OTHER_EMAIL":other_email,
            "WEBSITE": website
        }

        df_master_o = pd.DataFrame([update_request])
        df_master_o = replace_empty(df_master_o)
        df_master = preprocess_contacts_input(df_master_o, 'MASTER')
        df_master = df_master.replace('nan', '', regex=True)
        df_master = df_master.replace('not available', '', regex=True)

        processed_entry = df_master.to_dict('records')[0]

        update_query = {
            "$set": processed_entry
        }

        try:

            result = mongo.db.master_index_contacts.update_one(query, update_query)

            if result.matched_count > 0:
                response = {
                    "status": "Success",
                    "request_id": request_id,
                    "info": {
                        "message": f"Successfully Updated 1 Record",
                        "updated PartyRoleID": party_role_id,
                        "updated record query": update_query["$set"]
                    }
                }

                transaction = {
                    "_id": str(uuid.uuid4()),
                    "REQUEST_ID": request_id,
                    "TRANSACTION_COUNT": 1,
                    "API": "Contacts - Update Single Entry",
                    "CREATED_ON": datetime.utcnow().timestamp(),
                }

                mongo.db.master_index_contacts.insert_one(transaction)

                print("Clearing Cache")
                cache.clear()
                print("Cache Cleared")

                _ = reload_master_contacts_to_memory()
                return jsonify(response)

            else:
                response = {
                    "status": "Success",
                    "request_id": request_id,
                    "info": {
                        "message": "Contact not found",

                    }
                }
                return jsonify(response)

        except Exception as e:
            logger.error(e)
            response = {
                "status": "Success",
                "request_id": request_id,
                "info": {
                    "message": e,

                }
            }

            return jsonify(response)
