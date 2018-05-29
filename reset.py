import aws.iam.groups

for group in aws.iam.groups.get_groups():
    if group != "administrator":
        aws.iam.groups.delete_group(group)
